from sqlmodel import Session, select
from sqlmodel import and_

from app.schemas.teacher import *


def read_teacher(session: Session, teacher_id: int) -> Optional[Teacher]:
    statement = select(Teacher).where(and_(Teacher.id == teacher_id, Teacher.deleted_at is not None))
    return session.exec(statement).first()


def read_teachers(session: Session, query: Optional[str] = None):
    where = [Teacher.deleted_at is not None]
    if query:
        where.append(Teacher.name.like('%' + query + '%'))

    statement = select(Teacher).where(*where)
    return session.exec(statement).all()
