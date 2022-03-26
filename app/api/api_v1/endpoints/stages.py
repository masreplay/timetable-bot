from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.Stage])
def read_stages(
        db: Session = Depends(get_db),
        p: PagingParams = Depends(paging),
        branch_id: UUID = Query(None),
        branch_name: str = Query(None)
) -> Any:
    """
    Retrieve stages.
    """
    stages = crud.stage.get_filter(db, skip=p.skip, limit=p.limit, branch_id=branch_id,
                                   branch_name=branch_name)
    return stages


@router.post("/", response_model=schemas.Stage)
def create_stage(
        *,
        db: Session = Depends(get_db),
        stage_in: schemas.StageCreate,
) -> Any:
    """
    Create new stage.
    """
    branch = crud.branch.get(db=db, id=stage_in.branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    stage = crud.stage.get_by_object(db, stage=stage_in)
    if stage:
        raise HTTPException(status_code=400, detail="Stage already exist")

    stage = crud.stage.create(db=db, obj_in=stage_in)
    return stage


@router.put("/{id}", response_model=schemas.Stage)
def update_stage(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        stage_in: schemas.StageUpdate,
) -> Any:
    """
    Update a stage.
    """

    branch = crud.branch.get(db=db, id=stage_in.branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    stage = crud.stage.get_by_object(db, stage=stage_in)
    if stage:
        raise HTTPException(status_code=400, detail="Stage already exist")

    stage = crud.stage.get(db=db, id=id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    stage = crud.stage.update(db=db, db_obj=stage, obj_in=stage_in)
    return stage


@router.get("/{id}", response_model=schemas.Stage)
def read_stage(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get stage by ID.
    """
    stage = crud.stage.get(db=db, id=id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    return stage


@router.delete("/{id}", response_model=schemas.Stage)
def delete_stage(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a stage.
    """
    stage = crud.stage.get(db=db, id=id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    stage = crud.stage.remove(db=db, id=id)
    return stage
