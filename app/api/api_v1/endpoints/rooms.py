from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.Room])
def read_rooms(
        db: Session = Depends(get_db),
        p: PagingParams = Depends(paging),
) -> Any:
    """
    Retrieve rooms.
    """
    rooms = crud.room.get_multi(db, skip=p.skip, limit=p.limit)
    return rooms


@router.post("/", response_model=schemas.Room)
def create_room(
        *,
        db: Session = Depends(get_db),
        room_in: schemas.RoomCreate,
) -> Any:
    """
    Create new room.
    """
    building = crud.building.get(db=db, id=room_in.building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    floor = crud.floor.get(db=db, id=room_in.floor_id)
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")

    room = crud.room.create(db=db, obj_in=room_in)
    return room


@router.put("/{id}", response_model=schemas.Room)
def update_room(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        room_in: schemas.RoomUpdate,
) -> Any:
    """
    Update a room.
    """
    room = crud.room.get(db=db, id=id)
    if not room:
        raise HTTPException(status_code=404, detail="room not found")

    building = crud.building.get(db=db, id=room_in.building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    floor = crud.floor.get(db=db, id=room_in.floor_id)
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")

    room = crud.room.update(db=db, db_obj=room, obj_in=room_in)
    return room


@router.get("/{id}", response_model=schemas.Room)
def read_room(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get room by ID.
    """
    room = crud.room.get(db=db, id=id)
    if not room:
        raise HTTPException(status_code=404, detail="room not found")
    return room


@router.delete("/{id}", response_model=schemas.Room)
def delete_room(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a room.
    """
    room = crud.room.get(db=db, id=id)
    if not room:
        raise HTTPException(status_code=404, detail="room not found")
    room = crud.room.remove(db=db, id=id)
    return room
