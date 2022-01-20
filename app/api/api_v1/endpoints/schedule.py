from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.schedule import ScheduleDetails

router = APIRouter()


@router.get("/", response_model=schemas.ScheduleSchemas)
def read_all_schedule(
        db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve all schedules data.
    """
    return crud.schedule.get_multi(db=db)


@router.get("/stage/{stage_id}", response_model=ScheduleDetails)
def read_schedule(
        stage_id: UUID,
        db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve Single schedule.
    """
    stage = crud.stage.get(db=db, id=stage_id)
    if not stage:
        raise HTTPException(status_code=204, detail="Stage not found")
    return crud.schedule.get(db=db, stage_id=stage_id)
