from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.api import deps
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter(dependencies=[Depends(deps.PermissionHandler("periods"))])


@router.get("/", response_model=Paging[schemas.Period])
def read_periods(
        db: Session = Depends(get_db),
        p: PagingParams = Depends(paging),
) -> Any:
    """
    Retrieve periods.
    """
    periods = crud.period.get_multi(db, skip=p.skip, limit=p.limit)
    return periods


@router.post("/", response_model=schemas.Period)
def create_period(
        *,
        db: Session = Depends(get_db),
        period_in: schemas.PeriodCreate,
) -> Any:
    """
    Create new period.
    """
    period = crud.period.create(db=db, obj_in=period_in)
    return period


@router.put("/{id}", response_model=schemas.Period)
def update_period(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        period_in: schemas.PeriodUpdate,
) -> Any:
    """
    Update a period.
    """
    period = crud.period.get(db=db, id=id)
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    period = crud.period.update(db=db, db_obj=period, obj_in=period_in)
    return period


@router.get("/{id}", response_model=schemas.Period)
def read_period(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get period by ID.
    """
    period = crud.period.get(db=db, id=id)
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    return period


@router.delete("/{id}", response_model=schemas.Message)
def delete_period(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a period.
    """
    period = crud.period.get(db=db, id=id)
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    crud.period.remove(db=db, id=id)
    return schemas.Message(detail="Period deleted")
