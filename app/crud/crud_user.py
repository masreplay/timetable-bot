from typing import Any
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Session, select, col

from app import schemas, models
from app.core.security import verify_password, get_password_hash
from app.crud.base import CRUDBase
from app.models import User, UserJobTitle
from app.schemas.enums import UserType
from app.schemas.paging import Paging
from app.schemas.user import UserCreateDB, UserUpdate, UserCreate


class CRUDUser(CRUDBase[User, UserCreateDB, UserUpdate, schemas.User]):

    def get(self, db: Session, id: UUID) -> User | None:
        statement = select(self.model).where(User.id == id)
        return db.exec(statement).first()

    def get_by_name(self, db: Session, name: str) -> User | None:
        statement = select(self.model).where(User.name == name)
        return db.exec(statement).first()

    def get_by_email(self, db: Session, email: EmailStr) -> User | None:
        statement = select(self.model).where(User.email == email)
        return db.exec(statement).first()

    def update_job_titles(self, db: Session, id: UUID, job_titles: list[models.JobTitle]) -> User:
        user = self.get(db, id=id)
        for jt in job_titles:
            user.job_titles.append(jt)
            db.add(user)

        db.commit()
        db.refresh(user)
        return user

    def create_relation(self, *, db: Session, obj_in: UserCreate, image_url: str) -> User:
        db_obj = User(
            **UserCreateDB(**obj_in.dict(), image_url=image_url).dict(),
            hashed_password=get_password_hash(obj_in.password) if obj_in.password else None,
        )
        db.add(db_obj)

        for job_title in obj_in.job_titles:
            db.add(UserJobTitle(job_title_id=job_title, user_id=db_obj.id))
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_filter(
            self,
            db: Session, *,
            skip: int = 0,
            limit: int = 100,
            query: str | None,
            role_id: UUID | None,
            job_titles: list[UUID] | None,
            user_types: list[UserType] | None,
    ) -> Paging[schemas.User]:
        where = []
        if query:
            where.append(col(User.name).like('%' + query + '%'))
        if role_id:
            where.append(User.role_id == role_id)

        if job_titles:
            where.append(User.job_titles.any(models.JobTitle.id.in_(job_titles)))

        if user_types:
            where.append(User.job_titles.any(models.JobTitle.type.in_([user_type.name for user_type in user_types])))

        return Paging[schemas.User](
            count=db.query(User).filter(*where).count(),
            results=db.exec(select(User).order_by(User.name).where(*where).offset(skip).limit(limit)).all()
        )

    def update(
            self,
            db: Session,
            *,
            db_obj: User,
            obj_in: UserUpdate | dict[str, Any],
            job_titles: list[UUID] = []
    ) -> schemas.User:
        user_db = super().update(db=db, db_obj=db_obj, obj_in=obj_in)

        self.remove_job_titles(db=db, user=user_db)
        for job_title in job_titles:
            db.add(UserJobTitle(job_title_id=job_title, user_id=db_obj.id))

        db.commit()
        db.refresh(user_db)
        return user_db

    def authenticate(self, db: Session, *, email: EmailStr, password: str) -> User | None:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def remove_job_titles(self, db: Session, user: User) -> Any:
        user.job_titles = []
        db.commit()

    def is_active(self, user: User) -> bool:
        return user.is_active


user = CRUDUser(User, schemas.User)
