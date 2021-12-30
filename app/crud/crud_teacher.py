from typing import List

from sqlmodel import Session, select, col
from sqlmodel import and_

from app.crud.base import CRUDBase
from app.schemas.teacher import *


class CRUDTeacher(CRUDBase[Teacher, TeacherCreate, TeacherCreate]):

    def get(self, db: Session, id: int) -> Teacher:
        statement = select(self.model).where(and_(Teacher.id == id, Teacher.deleted_at is not None))
        return db.exec(statement).first()

    def get_filter(
            self, db: Session, *, skip: int = 0, limit: int = 100, query: str = None
    ) -> List[Teacher]:
        where = [Teacher.deleted_at is not None]
        if query:
            where.append(col(Teacher.name).like('%' + query + '%'))

        statement = select(Teacher).where(*where).offset(skip).limit(limit)
        return db.exec(statement).all()


teacher = CRUDTeacher(model=Teacher)
