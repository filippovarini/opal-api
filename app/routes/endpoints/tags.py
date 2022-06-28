from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Response, status, Request
from pydantic import BaseModel
from controllers.tagController import controller
from controllers.userController import userController

router = APIRouter()

class SavedSearchTag(BaseModel):
  tag_name: str
  result_ids: Optional[List[str]] = []       # list of result ids
  search: Optional[Dict[str, Any]] = []

@router.get("/{tag_substring}")
async def tags_from_substring(tag_substring: str, request: Request, response: Response):
  user = await userController.auth_user_with_request(request)
  if user is None:
    response.status_code = status.HTTP_401_UNAUTHORIZED

  return {"tags": await controller.get_from_substring(tag_substring, username=user['username'])}

@router.get("/{tag_category}/{tag_substring}")
async def tags_from_substring_from_category(tag_category: str, tag_substring: str):
  tags = await controller.get_from_substring(tag_substring, category=tag_category)

@router.post("/")
def tags_from_id(ids: List[str], response: Response):
  tags = controller.get_from_ids(ids)
  if (len(tags) == len(ids)):
    return {"tags": tags}
  else:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "Some ids are invalid!"}

@router.post("/create_tag")
async def create_tag(saved_search_tag: SavedSearchTag, request: Request):
  username = request.headers.get('username')
  password = request.headers.get('password')
  success_status = False
  if username is not None and password is not None:
    # check if username and password is correct
    if await userController.auth_user(username, password):
      success_status = True
      await controller.add_search_tag(username, saved_search_tag.tag_name, saved_search_tag.result_ids, saved_search_tag.search)
  return {"success": success_status}
  
  
  
