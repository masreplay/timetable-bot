from uuid import UUID

from pydantic import validator
from sqlmodel import Relationship, SQLModel, Field, Column, JSON

from app.schemas.base import BaseSchema
from app.schemas.branch import BranchBase
from app.schemas.building import BuildingBase
from app.schemas.card import CardBase
from app.schemas.department import DepartmentBase
from app.schemas.floor import FloorBase
from app.schemas.job_title import JobTitleBase
from app.schemas.lesson import LessonBase
from app.schemas.period import PeriodBase
from app.schemas.permissions import default_permissions, Permissions
from app.schemas.role import RoleBase
from app.schemas.room import RoomBase
from app.schemas.stage import StageBase
from app.schemas.subject import SubjectBase
from app.schemas.user import UserBase


class UserJobTitle(SQLModel, table=True):
    __tablename__ = "user_job_title"
    __name__ = "user_job_title"
    job_title_id: UUID | None = Field(
        default=None, foreign_key="job_title.id", primary_key=True
    )
    user_id: UUID | None = Field(
        default=None, foreign_key="user.id", primary_key=True
    )


class JobTitle(BaseSchema, JobTitleBase, table=True):
    __tablename__ = "job_title"
    __name__ = "job_title"
    users: list["User"] = Relationship(back_populates="job_titles", link_model=UserJobTitle)


class User(UserBase, BaseSchema, table=True):
    job_titles: list["JobTitle"] = Relationship(back_populates="users", link_model=UserJobTitle)
    hashed_password: str | None = Field(None)

    class Config:
        orm_mode = True


class Role(BaseSchema, RoleBase, table=True):
    permissions: dict = Field(sa_column=Column(JSON), default_factory=default_permissions.dict)

    @validator('permissions', pre=True, always=True)
    def permissions_validate(cls, v: dict | Permissions):
        if isinstance(v, Permissions):
            return v.dict()
        elif isinstance(v, dict):
            v = Permissions(**v)
            return v.dict()
        raise ValueError(v)

    @property
    def permissions_(self):
        return Permissions(**self.permissions)


class Period(BaseSchema, PeriodBase, table=True):
    pass


class Department(BaseSchema, DepartmentBase, table=True):
    branches: list["Branch"] = Relationship(back_populates="department")


class Branch(BaseSchema, BranchBase, table=True):
    department: "Department" = Relationship(back_populates="branches")
    stages: list["Stage"] = Relationship(back_populates="branch")


class Stage(BaseSchema, StageBase, table=True):
    branch: "Branch" = Relationship(back_populates="stages")


class Building(BaseSchema, BuildingBase, table=True):
    rooms: list["Room"] = Relationship(back_populates="building")


class Room(BaseSchema, RoomBase, table=True):
    building: "Building" = Relationship(back_populates="rooms")
    floor: "Floor" = Relationship(back_populates="rooms")


class Floor(BaseSchema, FloorBase, table=True):
    rooms: list["Room"] = Relationship(back_populates="floor")


class Card(BaseSchema, CardBase, table=True):
    pass


class Lesson(BaseSchema, LessonBase, table=True):
    pass


class Subject(BaseSchema, SubjectBase, table=True):
    pass
