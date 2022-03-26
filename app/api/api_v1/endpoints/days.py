from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.Day])
def read_days(
        db: Session = Depends(get_db),
        p: PagingParams = Depends(paging),
) -> Any:
    """
    Retrieve days.
    """
    days = crud.day.get_multi(db, skip=p.skip, limit=p.limit)
    return days


@router.post("/", response_model=schemas.Day)
def create_day(
        *,
        db: Session = Depends(get_db),
        day_in: schemas.DayCreate,
) -> Any:
    """
    Create new day.
    """
    day = crud.day.create(db=db, obj_in=day_in)
    return day


@router.put("/{id}", response_model=schemas.Day)
def update_day(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        day_in: schemas.DayUpdate,
) -> Any:
    """
    Update a day.
    """
    day = crud.day.get(db=db, id=id)
    if not day:
        raise HTTPException(status_code=404, detail="day not found")
    day = crud.day.update(db=db, db_obj=day, obj_in=day_in)
    return day


@router.get("/{id}", response_model=schemas.Day)
def read_day(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get day by ID.
    """
    day = crud.day.get(db=db, id=id)
    if not day:
        raise HTTPException(status_code=404, detail="day not found")
    return day


@router.delete("/{id}", response_model=schemas.Day)
def delete_day(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a day.
    """
    day = crud.day.get(db=db, id=id)
    if not day:
        raise HTTPException(status_code=404, detail="day not found")
    day = crud.day.remove(db=db, id=id)
    return day
