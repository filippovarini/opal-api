from fastapi import APIRouter, Response, status
from controllers.tagController import controller

router = APIRouter()

@router.get("/")
def tags_from_id(id: str, response: Response):
  tag = controller.get_from_id(id)
  if (tag):
    return {"tag": tag}
  else:
    response.status_code = status.HTTP_404_NOT_FOUND


@router.get("/{tag_substring}")
def tags_from_substring(tag_substring: str):
  return {"tags": controller.get_from_substring(tag_substring)}
