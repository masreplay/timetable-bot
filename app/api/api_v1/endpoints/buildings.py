from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.Building])
def read_buildings(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(50, ge=1, le=100),
) -> Any:
    """
    Retrieve buildings.
    """
    buildings = crud.building.get_multi(db, skip=skip, limit=limit)
    return buildings


@router.post("/", response_model=schemas.Building)
def create_building(
        *,
        db: Session = Depends(get_db),
        building_in: schemas.BuildingCreate,
) -> Any:
    """
    Create new building.
    """
    building = crud.building.create(db=db, obj_in=building_in)
    return building


@router.put("/{id}", response_model=schemas.Building)
def update_building(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        building_in: schemas.BuildingUpdate,
) -> Any:
    """
    Update a building.
    """
    building = crud.building.get(db=db, id=id)
    if not building:
        raise HTTPException(status_code=404, detail="building not found")
    building = crud.building.update(db=db, db_obj=building, obj_in=building_in)
    return building


@router.get("/{id}", response_model=schemas.Building)
def read_building(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get building by ID.
    """
    building = crud.building.get(db=db, id=id)
    if not building:
        raise HTTPException(status_code=404, detail="building not found")
    return building


@router.delete("/{id}", response_model=schemas.Building)
def delete_building(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a building.
    """
    building = crud.building.get(db=db, id=id)
    if not building:
        raise HTTPException(status_code=404, detail="building not found")
    building = crud.building.remove(db=db, id=id)
    return building
