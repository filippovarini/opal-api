from fastapi import APIRouter
from controllers.tagController import Tag, controller

router = APIRouter()

@router.get("/{tag_substring}")
def tags_from_substring(tag_substring: str):
  return {"tags": controller.get_from_substring(tag_substring)}