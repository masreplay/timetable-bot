from fastapi import APIRouter

from app.api.api_v1.endpoints import (users, roles, periods)

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(periods.router, prefix="/periods", tags=["periods"])
