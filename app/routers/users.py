from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.crud import user as crud
from app.db import get_session
from asc_scrapper.schemas import Teacher

router = APIRouter(
    prefix="/teachers",
    tags=["teacher"],
)


@router.get("/{teacher_id}", response_model=Teacher)
def get_teacher(teacher_id: int, session: Session = Depends(get_session)):
    crud.read_teacher(teacher_id=teacher_id, session=session)
