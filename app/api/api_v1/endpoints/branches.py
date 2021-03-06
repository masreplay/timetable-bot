from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.api.deps import PermissionHandler
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()
permissions = Depends(PermissionHandler("branches"))


@router.get("/", response_model=Paging[schemas.Branch])
def read_branches(
        db: Session = Depends(get_db),
        p: PagingParams = Depends(paging),
) -> Any:
    """
    Retrieve branches.
    """
    branches = crud.branch.get_multi(db, skip=p.skip, limit=p.limit)
    return branches


@router.post("/", response_model=schemas.Branch, dependencies=[permissions])
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


@router.put("/{id}", response_model=schemas.Branch, dependencies=[permissions])
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
        raise HTTPException(status_code=404, detail="Branch not found")
    branch = crud.branch.update(db=db, db_obj=branch, obj_in=branch_in)
    return branch


@router.get("/{id}", response_model=schemas.Branch, dependencies=[permissions])
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
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch


@router.delete("/{id}", response_model=schemas.Message, dependencies=[permissions])
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
        raise HTTPException(status_code=404, detail="Branch not found")
    crud.branch.remove(db=db, id=id)
    return schemas.Message(detail="Branch deleted")
