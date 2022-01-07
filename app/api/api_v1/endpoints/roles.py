from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.Role])
def read_roles(
        db: Session = Depends(get_db),
        paging: LimitSkipParams = Depends(),
) -> Any:
    """
    Retrieve roles.
    """
    roles = crud.role.get_multi(db, skip=paging.skip, limit=paging.limit)
    return roles


@router.post("/", response_model=schemas.Role)
def create_role(
        *,
        db: Session = Depends(get_db),
        role_in: schemas.RoleCreate,
) -> Any:
    """
    Create new role.
    """

    role = crud.role.create(db=db, obj_in=role_in)
    return role


@router.put("/{id}", response_model=schemas.Role)
def update_role(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        role_in: schemas.RoleUpdate,
) -> Any:
    """
    Update a role.
    """
    role = crud.role.get(db=db, id=id)
    if not role:
        raise HTTPException(status_code=404, detail="role not found")
    role = crud.role.update(db=db, db_obj=role, obj_in=role_in)
    return role


@router.get("/{id}", response_model=schemas.Role)
def read_role(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get role by ID.
    """
    role = crud.role.get(db=db, id=id)
    if not role:
        raise HTTPException(status_code=404, detail="role not found")
    return role


@router.delete("/{id}", response_model=schemas.Role)
def delete_role(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a role.
    """
    role = crud.role.get(db=db, id=id)
    if not role:
        raise HTTPException(status_code=404, detail="role not found")
    role = crud.role.remove(db=db, id=id)
    return role
