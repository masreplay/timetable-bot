from typing import Optional, List
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Session, select, col

from app import schemas, models
from app.core.security import verify_password, get_password_hash
from app.crud.base import CRUDBase
from app.models import User
from app.schemas.enums import UserType
from app.schemas.paging import Paging
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get(self, db: Session, id: UUID) -> User:
        statement = select(self.model).where(User.id == id)
        return db.exec(statement).first()

    def get_by_name(self, db: Session, name: str) -> Optional[User]:
        statement = select(self.model).where(User.name == name)
        return db.exec(statement).first()

    def get_by_email(self, db: Session, email: EmailStr) -> Optional[User]:
        statement = select(self.model).where(User.email == email)
        return db.exec(statement).first()

    def update_job_titles_by_email(self, db: Session, email: EmailStr, job_titles: List[models.JobTitle]) -> User:
        user = self.get_by_email(db, email=email)
        for jt in job_titles:
            user.job_titles.append(jt)
            db.add(user)

        db.commit()
        db.refresh(user)
        return user

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            **obj_in.dict(),
            hashed_password=get_password_hash(obj_in.password) if obj_in.password else None,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_filter(
            self, db: Session, *, skip: int = 0, limit: int = 100, query: Optional[str], role_id: Optional[UUID],
            user_type: Optional[UserType]
    ) -> Paging[schemas.User]:
        where = []
        if query:
            where.append(col(User.name).like('%' + query + '%'))
        if role_id:
            where.append(User.role_id == role_id)

        if user_type:
            where.append(User.job_titles.any(models.JobTitle.type == user_type))
        else:
            where.append(
                User.job_titles.any(
                    models.JobTitle.type == UserType.teacher and models.JobTitle.type == UserType.employee
                )
            )

        return Paging[schemas.User](
            count=db.query(User).filter(*where).count(),
            results=db.exec(select(User).where(*where).offset(skip).limit(limit)).all()
        )

    def authenticate(self, db: Session, *, email: EmailStr, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active


user = CRUDUser(User)
