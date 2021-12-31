from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import LimitSkipParams, Paging

router = APIRouter()


@router.get("/", response_model=Paging[schemas.User])
def read_users(
        db: Session = Depends(get_db),
        paging: LimitSkipParams = Depends(),
        query: Optional[str] = None,
        role_id: Optional[UUID] = None,
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_filter(db, skip=paging.skip, limit=paging.limit, query=query, role_id=role_id)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(get_db),
        user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.create(db=db, obj_in=user_in)
    return user


@router.put("/{id}", response_model=schemas.User)
def update_user(
        *,
        db: Session = Depends(get_db),
        id: int,
        user_in: schemas.UserUpdate,
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    user = crud.user.update(db=db, db_obj=user, obj_in=user_in)
    return user


@router.get("/{id}", response_model=schemas.User)
def read_user(
        *,
        db: Session = Depends(get_db),
        id: int,
) -> Any:
    """
    Get user by ID.
    """
    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.delete("/{id}", response_model=schemas.User)
def delete_user(
        *,
        db: Session = Depends(get_db),
        id: int,
) -> Any:
    """
    Delete a user.
    """
    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    user = crud.user.remove(db=db, id=id)
    return user


@router.delete("/", response_model=schemas.User)
def delete_users(
        *,
        db: Session = Depends(get_db),
) -> Any:
    """
    Delete all a users.
    """
    users: Paging[schemas.User] = crud.user.get_multi(db=db)
    for user in users.results:
        db.delete(user)

    db.commit()