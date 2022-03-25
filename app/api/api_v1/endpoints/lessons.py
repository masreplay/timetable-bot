from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.Lesson])
def read_lessons(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(50, ge=1, le=100),
) -> Any:
    """
    Retrieve lessons.
    """
    lessons = crud.lesson.get_multi(db, skip=skip, limit=limit)
    return lessons


@router.post("/", response_model=schemas.Lesson)
def create_lesson(
        *,
        db: Session = Depends(get_db),
        lesson_in: schemas.LessonCreate,
) -> Any:
    """
    Create new lesson.
    """
    lesson = crud.lesson.create(db=db, obj_in=lesson_in)
    return lesson


@router.put("/{id}", response_model=schemas.Lesson)
def update_lesson(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        lesson_in: schemas.LessonUpdate,
) -> Any:
    """
    Update a lesson.
    """
    lesson = crud.lesson.get(db=db, id=id)
    if not lesson:
        raise HTTPException(status_code=404, detail="lesson not found")
    lesson = crud.lesson.update(db=db, db_obj=lesson, obj_in=lesson_in)
    return lesson


@router.get("/{id}", response_model=schemas.Lesson)
def read_lesson(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get lesson by ID.
    """
    lesson = crud.lesson.get(db=db, id=id)
    if not lesson:
        raise HTTPException(status_code=404, detail="lesson not found")
    return lesson


@router.delete("/{id}", response_model=schemas.Lesson)
def delete_lesson(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a lesson.
    """
    lesson = crud.lesson.get(db=db, id=id)
    if not lesson:
        raise HTTPException(status_code=404, detail="lesson not found")
    lesson = crud.lesson.remove(db=db, id=id)
    return lesson
