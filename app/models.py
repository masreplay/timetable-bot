from typing import List
from uuid import UUID

from pydantic import validator
from sqlmodel import Relationship, SQLModel, Field, Column, JSON

from app.schemas.asc_version import AscVersionBase
from app.schemas.base import BaseSchema
from app.schemas.branch import BranchBase
from app.schemas.building import BuildingBase
from app.schemas.card import CardBase
from app.schemas.day import DayBase
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


class StageLesson(SQLModel, table=True):
    __tablename__ = "stage_lesson"
    __name__ = "stage_lesson"
    lesson_id: UUID | None = Field(
        default=None, foreign_key="lesson.id", primary_key=True
    )
    stage_id: UUID | None = Field(
        default=None, foreign_key="stage.id", primary_key=True
    )


class JobTitle(BaseSchema, JobTitleBase, table=True):
    __tablename__ = "job_title"
    __name__ = "job_title"
    users: List["User"] = Relationship(back_populates="job_titles", link_model=UserJobTitle)


class User(UserBase, BaseSchema, table=True):
    hashed_password: str | None = Field(default=None)

    lesson: "Lesson" = Relationship(back_populates="teacher")
    job_titles: List["JobTitle"] = Relationship(back_populates="users", link_model=UserJobTitle)

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
    branches: List["Branch"] = Relationship(back_populates="department")


class Branch(BaseSchema, BranchBase, table=True):
    department: "Department" = Relationship(back_populates="branches")
    stages: List["Stage"] = Relationship(back_populates="branch")


class Stage(BaseSchema, StageBase, table=True):
    branch: "Branch" = Relationship(back_populates="stages")

    lessons: List["Lesson"] = Relationship(back_populates="stages", link_model=StageLesson)

    class Config:
        orm_mode = True


class Building(BaseSchema, BuildingBase, table=True):
    rooms: List["Room"] = Relationship(back_populates="building")


class Room(BaseSchema, RoomBase, table=True):
    building: "Building" = Relationship(back_populates="rooms")
    lesson: "Lesson" = Relationship(back_populates="room")
    floor: "Floor" = Relationship(back_populates="rooms")


class Floor(BaseSchema, FloorBase, table=True):
    rooms: List["Room"] = Relationship(back_populates="floor")


class Card(BaseSchema, CardBase, table=True):
    lesson: "Lesson" = Relationship(back_populates="card")

    class Config:
        orm_mode = True


class Lesson(BaseSchema, LessonBase, table=True):
    card: Card = Relationship(back_populates="lesson")
    subject: "Subject" = Relationship(back_populates="lesson")
    teacher: "User" = Relationship(back_populates="lesson")
    room: "Room" = Relationship(back_populates="lesson")

    stages: List["Stage"] = Relationship(back_populates="lessons", link_model=StageLesson)


class Subject(BaseSchema, SubjectBase, table=True):
    lesson: "Lesson" = Relationship(back_populates="subject")


class Day(BaseSchema, DayBase, table=True):
    cards: List["Card"] = Relationship(
        sa_relationship_kwargs={"cascade": "delete"}
    )


class AscVersion(BaseSchema, AscVersionBase, table=True):
    pass
