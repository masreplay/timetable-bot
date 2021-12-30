from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.crud import user as crud
from app.db import get_session
from app.schemas.teacher import Teacher, TeacherCreate
from asc_scrapper.asc_data import db
from asc_scrapper.schemas import AscTeacher

router = APIRouter(
    prefix="/teachers",
    tags=["teacher"],
)


@router.get("/{teacher_id}", response_model=Teacher)
def get_teacher(teacher_id: int, session: Session = Depends(get_session)):
    return crud.read_teacher(teacher_id=teacher_id, session=session)


@router.get("/", response_model=List[Teacher])
def get_teachers(query: Optional[str] = None, session: Session = Depends(get_session)):
    return crud.read_teachers(query=query, session=session)


@router.patch("/", )
def create_teachers(session: Session = Depends(get_session)):
    asc_teachers: list[AscTeacher] = db.get_teachers()

    for asc_teacher in asc_teachers:
        teacher = Teacher(name=asc_teacher.short)
        session.add(teacher)

    session.commit()
    session.close()


@router.delete("/")
def delete_teachers(session: Session = Depends(get_session)):
    teachers = crud.read_teachers(session=session)
    for teacher in teachers:
        session.delete(teacher)
    session.commit()
    session.close()
