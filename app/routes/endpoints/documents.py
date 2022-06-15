from ast import keyword
from curses import meta
from typing import Dict, List
from fastapi import APIRouter
from controllers.documents import UserSearch, documentController as documents

router = APIRouter()
  
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
def search_documents(user_search: UserSearch):
  meta_docs = documents.get_from_metadata(user_search.tags, user_search.fields)
  keyword_docs = documents.get_from_keywords(user_search.keywords)

  return {"docs": document_union(meta_docs, keyword_docs), "meta": meta_docs}
