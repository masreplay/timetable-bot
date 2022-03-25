from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.Floor])
def read_floors(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(50, ge=1, le=100),
) -> Any:
    """
    Retrieve floors.
    """
    floors = crud.floor.get_multi(db, skip=skip, limit=limit)
    return floors


@router.post("/", response_model=schemas.Floor)
def create_floor(
        *,
        db: Session = Depends(get_db),
        floor_in: schemas.FloorCreate,
) -> Any:
    """
    Create new floor.
    """
    floor = crud.floor.create(db=db, obj_in=floor_in)
    return floor


@router.put("/{id}", response_model=schemas.Floor)
def update_floor(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        floor_in: schemas.FloorUpdate,
) -> Any:
    """
    Update a floor.
    """
    floor = crud.floor.get(db=db, id=id)
    if not floor:
        raise HTTPException(status_code=404, detail="floor not found")
    floor = crud.floor.update(db=db, db_obj=floor, obj_in=floor_in)
    return floor


@router.get("/{id}", response_model=schemas.Floor)
def read_floor(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get floor by ID.
    """
    floor = crud.floor.get(db=db, id=id)
    if not floor:
        raise HTTPException(status_code=404, detail="floor not found")
    return floor


@router.delete("/{id}", response_model=schemas.Floor)
def delete_floor(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a floor.
    """
    floor = crud.floor.get(db=db, id=id)
    if not floor:
        raise HTTPException(status_code=404, detail="floor not found")
    floor = crud.floor.remove(db=db, id=id)
    return floor
