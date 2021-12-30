from fastapi import APIRouter

from app.api.api_v1.endpoints import teachers

api_router = APIRouter()
api_router.include_router(teachers.router, tags=["teachers"])
