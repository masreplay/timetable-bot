from typing import Optional, List, Any
from uuid import UUID

from sqlmodel import Session, select, col

from app import schemas
from app.core.security import verify_password, get_password_hash
from app.crud.base import CRUDBase
from app.models import User
from app.schemas.paging import Paging
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get(self, db: Session, id: UUID) -> User:
        statement = select(self.model).where(User.id == id)
        return db.exec(statement).first()

    def get_by_name(self, db: Session, name: str) -> Optional[User]:
        statement = select(self.model).where(User.name == name)
        return db.exec(statement).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        statement = select(self.model).where(User.email == email)
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            hashed_password=get_password_hash(obj_in.password) if obj_in.password is not None else None,
            **obj_in.dict()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_filter(
            self, db: Session, *, skip: int = 0, limit: int = 100, query: str = None, role_id: UUID = None
    ) -> Paging[schemas.User]:
        where = []
        if query:
            where.append(col(User.name).like('%' + query + '%'))

        if role_id:
            where.append(User.role_id == role_id)
        return Paging[schemas.User](
            count=db.query(User).filter(*where).count(),
            results=db.exec(select(User).where(*where).offset(skip).limit(limit)).all()
        )

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active


user = CRUDUser(User)
