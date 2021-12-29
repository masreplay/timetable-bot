from typing import Optional

from sqlmodel import Session, select
from sqlmodel import and_

from app.schemas.teacher import *


def read_teacher(teacher_id: int, session: Session) -> Optional[Teacher]:
    statement = select(Teacher).where(and_(Teacher.id == teacher_id, Teacher.deleted_at is not None))
    return session.exec(statement).first()
