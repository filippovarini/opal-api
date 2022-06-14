from fastapi import APIRouter

from routes.endpoints import search

api_router = APIRouter()

api_router.include_router(search.router, prefix='/search', tags=['search'])