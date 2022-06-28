from typing import List, Dict
from fastapi import APIRouter, Response, status, Request
from controllers.tagController import controller
from controllers.userController import userController

router = APIRouter()

@router.get("/{tag_substring}")
async def tags_from_substring(tag_substring: str, request: Request, response: Response):
  user = await userController.auth_user_with_request(request)
  if user is None:
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
