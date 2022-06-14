from fastapi import APIRouter
from controllers.search import searchController as controller
router = APIRouter()

@router.get("/")
def greet():
  return {'response': controller.get_documents()}
