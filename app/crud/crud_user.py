from sqlmodel import Session, select, col, and_

from app.schemas.paging import Paging
from app.crud.base import CRUDBase
from app.schemas.user import *


class CRUDUser(CRUDBase[User, UserCreate, UserCreate]):

    def get(self, db: Session, id: int) -> User:
        statement = select(self.model).where(and_(User.id == id, User.deleted_at is not None))
        return db.exec(statement).first()

    def get_by_name(self, db: Session, name: str) -> User:
        statement = select(self.model).where(and_(User.ar_name == name, User.deleted_at is not None))
        return db.exec(statement).first()

    def get_filter(
            self, db: Session, *, skip: int = 0, limit: int = 100, query: str = None, role_id: str = None
    ) -> Paging[User]:
        where = [User.deleted_at is not None]
        if query:
            where.append(col(User.ar_name).like('%' + query + '%'))

        if role_id:
            where.append(User.role_id == role_id)

        statement = select(User)
        return Paging[User](
            count=db.query(User).count(),
            results=db.exec(statement.where(*where).offset(skip).limit(limit)).all(),
        )


user = CRUDUser(User)
