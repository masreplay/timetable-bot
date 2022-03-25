from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.Department])
def read_departments(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(50, ge=1, le=100),
) -> Any:
    """
    Retrieve departments.
    """
    departments = crud.department.get_multi(db, skip=skip, limit=limit)
    return departments


@router.post("/", response_model=schemas.Department)
def create_department(
        *,
        db: Session = Depends(get_db),
        department_in: schemas.DepartmentCreate,
) -> Any:
    """
    Create new department.
    """
    department = crud.department.create(db=db, obj_in=department_in)
    return department


@router.put("/{id}", response_model=schemas.Department)
def update_department(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        department_in: schemas.DepartmentUpdate,
) -> Any:
    """
    Update a department.
    """
    department = crud.department.get(db=db, id=id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    department = crud.department.update(db=db, db_obj=department, obj_in=department_in)
    return department


@router.get("/{id}", response_model=schemas.Department)
def read_department(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get department by ID.
    """
    department = crud.department.get(db=db, id=id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.delete("/{id}", response_model=schemas.Department)
def delete_department(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a department.
    """
    department = crud.department.get(db=db, id=id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    department = crud.department.remove(db=db, id=id)
    return department
