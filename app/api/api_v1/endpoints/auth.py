from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.deps import UserRole
from app.core import security
from app.db.db import get_db, settings

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    return schemas.Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )


# @router.post("/signup", response_model=schemas.Message)
# def sign_up(user: schemas.UserCreateDB, db: Session = Depends(get_db)) -> Any:
#     """
#     User create new account, get an access token for future requests
#     """
#     old_user = crud.user.get_by_email(db, email=user.email)
#     if old_user:
#         raise HTTPException(status_code=401, detail="User already exist")
#
#     crud.user.create(db, obj_in=user)
#
#     return schemas.Message(detail="User have been created")


@router.get("/permissions/", response_model=schemas.Role)
def get_my_permissions(permissions: UserRole = Depends(deps.users_permission_handler)) -> Any:
    """
    Return my permissions
    """

    return permissions.role


# @router.post("/reset-password/", response_model=schemas.Message)
# def reset_password(
#         token: str = Body(...),
#         new_password: str = Body(...),
#         db: Session = Depends(get_db),
# ) -> Any:
#     """
#     Reset password
#     """
#     email = verify_password_reset_token(token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user = crud.user.get_by_email(db, email=email)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     elif not crud.user.is_active(user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     hashed_password = get_password_hash(new_password)
#     user.hashed_password = hashed_password
#     db.add(user)
#     db.commit()
#     return schemas.Message(detail="Password updated successfully")
