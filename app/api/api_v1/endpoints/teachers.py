from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.schemas.paging import LimitSkipParams, Paging
from app.db.db import get_db
from app.schemas import Teacher

router = APIRouter()


@router.get("/", response_model=Paging[schemas.Teacher])
def read_teachers(
        db: Session = Depends(get_db),
        paging: LimitSkipParams = Depends(),
        query: Optional[str] = None,
        role_id: Optional[UUID] = None,
) -> Any:
    """
    Retrieve teachers.
    """
    teachers = crud.teacher.get_filter(db, skip=paging.skip, limit=paging.limit, query=query, role_id=role_id)
    return teachers


@router.post("/", response_model=schemas.Teacher)
def create_teacher(
        *,
        db: Session = Depends(get_db),
        teacher_in: schemas.TeacherCreate,
) -> Any:
    """
    Create new teacher.
    """
    teacher = crud.teacher.create(db=db, obj_in=teacher_in)
    return teacher


@router.put("/{id}", response_model=schemas.Teacher)
def update_teacher(
        *,
        db: Session = Depends(get_db),
        id: int,
        teacher_in: schemas.TeacherUpdate,
) -> Any:
    """
    Update a teacher.
    """
    teacher = crud.teacher.get(db=db, id=id)
    if not teacher:
        raise HTTPException(status_code=404, detail="teacher not found")
    teacher = crud.teacher.update(db=db, db_obj=teacher, obj_in=teacher_in)
    return teacher


@router.get("/{id}", response_model=schemas.Teacher)
def read_teacher(
        *,
        db: Session = Depends(get_db),
        id: int,
) -> Any:
    """
    Get teacher by ID.
    """
    teacher = crud.teacher.get(db=db, id=id)
    if not teacher:
        raise HTTPException(status_code=404, detail="teacher not found")
    return teacher


@router.delete("/{id}", response_model=schemas.Teacher)
def delete_teacher(
        *,
        db: Session = Depends(get_db),
        id: int,
) -> Any:
    """
    Delete a teacher.
    """
    teacher = crud.teacher.get(db=db, id=id)
    if not teacher:
        raise HTTPException(status_code=404, detail="teacher not found")
    teacher = crud.teacher.remove(db=db, id=id)
    return teacher


@router.delete("/", response_model=schemas.Teacher)
def delete_teachers(
        *,
        db: Session = Depends(get_db),
) -> Any:
    """
    Delete all a teachers.
    """
    teachers: Paging[Teacher] = crud.teacher.get_multi(db=db)
    for teacher in teachers.results:
        db.delete(teacher)

    db.commit()
