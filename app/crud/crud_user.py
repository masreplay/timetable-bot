from typing import Optional
from uuid import UUID

from sqlalchemy import or_
from sqlmodel import Session, select, col, and_, not_

from app.core.security import verify_password, get_password_hash
from app.crud.base import CRUDBase
from app.schemas.paging import Paging
from app.schemas.user import (UserSchema, UserCreate)
from sqlalchemy.sql import column


class CRUDUser(CRUDBase[UserSchema, UserCreate, UserCreate]):

    def get(self, db: Session, id: UUID) -> UserSchema:
        statement = select(self.model).where(UserSchema.id == id)
        return db.exec(statement).first()

    def get_by_name(self, db: Session, name: str) -> Optional[UserSchema]:
        statement = select(self.model).where(UserSchema.name == name)
        return db.exec(statement).first()

    def get_by_email(self, db: Session, email: str) -> Optional[UserSchema]:
        statement = select(self.model).where(UserSchema.email == email)
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> UserSchema:
        db_obj = UserSchema(
            hashed_password=get_password_hash(obj_in.password) if obj_in.password is not None else None,
            **obj_in.dict()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_filter(
            self, db: Session, *, skip: int = 0, limit: int = 100, query: str = None, role_id: UUID = None
    ) -> Paging[UserSchema]:
        where = []
        if query:
            where.append(col(UserSchema.name).like('%' + query + '%'))

        if role_id:
            where.append(UserSchema.role_id == role_id)

        statement = select(UserSchema)
        return Paging[UserSchema](
            count=db.query(UserSchema).filter(*where).count(),
            results=db.exec(statement.where(*where).offset(skip).limit(limit)).all(),
        )

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[UserSchema]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: UserSchema) -> bool:
        return user.is_active


user = CRUDUser(UserSchema)
