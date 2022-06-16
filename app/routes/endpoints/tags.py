from typing import List
from fastapi import APIRouter, Response, status
from controllers.tagController import controller

router = APIRouter()

@router.get("/{tag_substring}")
def tags_from_substring(tag_substring: str):
  return {"tags": controller.get_from_substring(tag_substring)}

@router.post("/")
def tags_from_id(ids: List[str], response: Response):
  tags = controller.get_from_ids(ids)
  if (len(tags) == len(ids)):
    return {"tags": tags}
  else:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "Some ids are invalid!"}
