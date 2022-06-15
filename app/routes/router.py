from fastapi import APIRouter

from routes.endpoints import documents

api_router = APIRouter()

api_router.include_router(documents.router, prefix='/document', tags=['document'])