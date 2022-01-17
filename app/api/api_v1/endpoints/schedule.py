from typing import Any

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db

router = APIRouter()


@router.get("/", response_model=schemas.ScheduleSchemas)
def read_schedule(
        db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve schedule.

    """
    return crud.schedule.get(db=db)
