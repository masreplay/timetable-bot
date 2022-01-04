from enum import Enum
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core import security
from app.core.config import settings
from app.db.db import get_db
from app.schemas import Role

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings().API_V1_STR}/auth/login/access-token"
)


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> schemas.UserSchema:
    try:
        payload = jwt.decode(
            token, settings().SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
        current_user: schemas.UserSchema = Depends(get_current_user),
) -> schemas.UserSchema:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
        current_user: schemas.UserSchema = Depends(get_current_user),
) -> schemas.UserSchema:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


class PermissionMethod(str, Enum):
    """
    Additional permission method like GET, POST, PUT, PATCH and DELETE
    """
    suspend = "SUSPEND"


def method_to_permission_name(method: str):
    """
    Request method name to permission CRUD name
    """
    if method == "GET":
        return "read"
    elif method == "POST":
        return "create"
    elif method == "DELETE":
        return "delete"
    elif method == "PUT" or method == "PATCH":
        return "update"
    else:
        return method


class PermissionHandler:

    """
    Check if user have permission to preform this actions
    """

    def __init__(self, router: str, method: Optional[PermissionMethod] = None):
        self.method = method
        self.router = router

    def set_method(self, value: PermissionMethod):
        self.method = value

    async def __call__(
            self,
            request: Request,
            current_user: schemas.UserSchema = Depends(get_current_user),
            db: Session = Depends(get_db)
    ) -> Role:
        method = self.method.value if self.method else request.method

        print(f"METHOD: {method}")

        # user permission
        role: schemas.Role = crud.role.get(db, id=current_user.role_id)

        try:
            # Permissions for current router
            router_permission: Optional[dict] = role.permissions[self.router]

            # Permission name
            current_permission: str = method_to_permission_name(method)

            # Does user have this permission
            have_permission: bool = router_permission[current_permission]

            if not have_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to preform this action",
                )

            return role

        except KeyError:
            print("Permission group not found")
            raise HTTPException(400, "Some error occurred")


users_permission_handler = PermissionHandler(router="users")
roles_permission_handler = PermissionHandler(router="roles")
