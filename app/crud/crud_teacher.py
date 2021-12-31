from sqlmodel import Session, select, col, and_

from app.schemas.paging import Paging
from app.crud.base import CRUDBase
from app.schemas.teacher import *


class CRUDTeacher(CRUDBase[Teacher, TeacherCreate, TeacherCreate]):

    def get(self, db: Session, id: int) -> Teacher:
        statement = select(self.model).where(and_(Teacher.id == id, Teacher.deleted_at is not None))
        return db.exec(statement).first()

    def get_by_name(self, db: Session, name: str) -> Teacher:
        statement = select(self.model).where(and_(Teacher.ar_name == name, Teacher.deleted_at is not None))
        return db.exec(statement).first()

    def get_filter(
            self, db: Session, *, skip: int = 0, limit: int = 100, query: str = None, role_id: str = None
    ) -> Paging[Teacher]:
        where = [Teacher.deleted_at is not None]
        if query:
            where.append(col(Teacher.ar_name).like('%' + query + '%'))

        if role_id:
            where.append(Teacher.role_id == role_id)

        statement = select(Teacher)
        return Paging[Teacher](
            count=db.query(Teacher).count(),
            results=db.exec(statement.where(*where).offset(skip).limit(limit)).all(),
        )


teacher = CRUDTeacher(Teacher)
