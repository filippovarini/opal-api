from optparse import Option
from typing import Optional, List
from controllers.docController import DocumentController
from controllers.userController import userController
from pydantic import BaseModel
from fastapi import APIRouter, Request
from controllers.docController import documentController as documents
from assets.document import DocumentFields
from assets.user import User
from db.db_controller import SearchQuery

router = APIRouter()

# Type model of User Search request body
class UserSearch(BaseModel):
  tags: Optional[List[str]] = []       # list of tag ids
  keywords: Optional[List[str]] = []
  fields: Optional[DocumentFields] = {}

# Type model of an access request for a document
class AccessRequest(BaseModel):
  document_id: str
  reason: Optional[str] = ""

class AccessGrant(BaseModel):
  document_id: str
  granted_to: str

  
# Given two independent document searches represented as array of same Document 
# object, union them
def document_union(meta_docs, keyword_docs):
  # TODO: implement properly
  return meta_docs


# Gets a request based on FIELDS, TAGS and KEYWORDS. 
# From that, performs 2 different searches:
# 1) From our own DB based on TAGs and FIELDS
# 2) Independent (ouw DB or others) based on the KEYWORDS
# That is because for keyword search we need access to the Document text,
# and not all companies might give it to us.
@router.post("/")
async def search_documents(user_search: UserSearch):
  meta_docs = await documents.get_from_metadata(user_search.tags, user_search.fields)
  
  # TODO: implement saerch by keyword
  keyword_docs = documents.get_from_keywords(user_search.keywords)

  return {"docs": document_union(meta_docs, keyword_docs), "meta": meta_docs}

@router.post("/requestaccess")
async def request_access(request: Request, access_request: AccessRequest):
  user = await userController.auth_user_with_request(request)
  if user is None:
    return {"success": False}
  await userController.request_document_access(user['username'], access_request.document_id, access_request.reason)
  return {"success": True}

@router.post("/grantaccess")
async def grant_access(request: Request, access_grant: AccessGrant):
  user = await userController.auth_user_with_request(request)
  if user is None or user['role'] != "admin":
    return {"success": False}
  await documents.grant_access_to(access_grant.granted_to, access_grant.document_id)
  await user.notify_of_access_grant(access_grant.granted_to, access_grant.document_id)
  return {"success": True}
  

@router.post("/search")
async def search(search_query: SearchQuery):
  print(search_query)
  results = await documents.get_from_search_query(search_query)
  return {"docs": results, "meta": []}
