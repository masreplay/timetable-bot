from fastapi import APIRouter

from app.api.api_v1.endpoints import (teachers, roles)

api_router = APIRouter()
api_router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
