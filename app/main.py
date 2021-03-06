from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.router import api_router
from core.config import settings

app = FastAPI()

ORIGINS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix=settings.API_V1_STR)
