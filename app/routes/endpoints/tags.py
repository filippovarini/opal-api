from typing import List, Dict
from fastapi import APIRouter, Response, status, Request
from controllers.tagController import controller
from controllers.userController import userController

router = APIRouter()

@router.get("/{tag_substring}")
async def tags_from_substring(tag_substring: str, request: Request, response: Response):
  username = request.headers.get('username')
  password = request.headers.get('password')
  if username is not None and password is not None:
    # check if username and password is correct
    if not await userController.auth_user(username, password):
      response.status_code = status.HTTP_401_UNAUTHORIZED
      username = None

  return {"tags": controller.get_from_substring(tag_substring, username=username)}

@router.post("/")
def tags_from_id(ids: List[str], response: Response):
  tags = controller.get_from_ids(ids)
  # if (len(tags) == len(ids)):
  return {"tags": tags}
  # else:
  #   response.status_code = status.HTTP_404_NOT_FOUND
  #   return {"message": "Some ids are invalid!"}
