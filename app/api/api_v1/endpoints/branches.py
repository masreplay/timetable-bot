from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.Branch])
def read_branches(
        db: Session = Depends(get_db),
        paging: LimitSkipParams = Depends(),
) -> Any:
    """
    Retrieve branches.
    """
    branches = crud.branch.get_multi(db, skip=paging.skip, limit=paging.limit)
    return branches


@router.post("/", response_model=schemas.Branch)
def create_branch(
        *,
        db: Session = Depends(get_db),
        branch_in: schemas.BranchCreate,
) -> Any:
    """
    Create new branch.
    """
    branch = crud.branch.create(db=db, obj_in=branch_in)
    return branch


@router.put("/{id}", response_model=schemas.Branch)
def update_branch(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        branch_in: schemas.BranchUpdate,
) -> Any:
    """
    Update a branch.
    """
    branch = crud.branch.get(db=db, id=id)
    if not branch:
        raise HTTPException(status_code=404, detail="branch not found")
    branch = crud.branch.update(db=db, db_obj=branch, obj_in=branch_in)
    return branch


@router.get("/{id}", response_model=schemas.Branch)
def read_branch(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get branch by ID.
    """
    branch = crud.branch.get(db=db, id=id)
    if not branch:
        raise HTTPException(status_code=404, detail="branch not found")
    return branch


@router.delete("/{id}", response_model=schemas.Branch)
def delete_branch(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a branch.
    """
    branch = crud.branch.get(db=db, id=id)
    if not branch:
        raise HTTPException(status_code=404, detail="branch not found")
    branch = crud.branch.remove(db=db, id=id)
    return branch
