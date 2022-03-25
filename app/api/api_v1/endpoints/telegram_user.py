from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.TelegramUser])
def read_telegram_users(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(50, ge=1, le=100),
) -> Any:
    """
    Retrieve telegram_users.
    """

    telegram_users = crud.telegram_user.get_multi(db, skip=skip, limit=limit)
    return telegram_users


@router.post("/", response_model=schemas.TelegramUser)
def create_telegram_user(
        *,
        db: Session = Depends(get_db),
        telegram_user_in: schemas.TelegramUserCreate,
) -> Any:
    """
    Create new telegram_user.
    """
    telegram_user = crud.telegram_user.create(db=db, obj_in=telegram_user_in)
    return telegram_user


@router.put("/{id}", response_model=schemas.TelegramUser)
def update_telegram_user(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        telegram_user_in: schemas.TelegramUserUpdate,
) -> Any:
    """
    Update a telegram_user.
    """
    telegram_user = crud.telegram_user.get(db=db, id=id)
    if not telegram_user:
        raise HTTPException(status_code=404, detail="user not found")
    telegram_user = crud.telegram_user.update(db=db, db_obj=telegram_user, obj_in=telegram_user_in)
    return telegram_user


@router.get("/{id}", response_model=schemas.TelegramUser)
def read_telegram_user(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get telegram_user by ID.
    """
    telegram_user = crud.telegram_user.get(db=db, id=id)
    if not telegram_user:
        raise HTTPException(status_code=404, detail="user not found")
    return telegram_user


@router.delete("/{id}", response_model=schemas.TelegramUser)
def delete_telegram_user(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a telegram_user.
    """
    telegram_user = crud.telegram_user.get(db=db, id=id)
    if not telegram_user:
        raise HTTPException(status_code=404, detail="user not found")
    telegram_user = crud.telegram_user.remove(db=db, id=id)
    return telegram_user
