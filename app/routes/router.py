from fastapi import APIRouter
from routes.endpoints import documents
from routes.endpoints import tags
from routes.endpoints import users

api_router = APIRouter()

api_router.include_router(documents.router, prefix='/document', tags=['documents'])
api_router.include_router(tags.router, prefix='/tags', tags=['tags'])
api_router.include_router(users.router, prefix='/users', tags=['users'])