from uuid import UUID
from enum import Enum
from typing import Optional

from pydantic import AnyHttpUrl
from sqlmodel import SQLModel, Field

from app.schemas.base_model import BaseSchema


class UserType(str, Enum):
    employee = "employee"
    teacher = "teacher"
    student = "student"
    other = "other"


class TeacherBase(SQLModel):
    en_name: str = Field(index=True)
    ar_name: str = Field(index=True)
    role_id: UUID = Field(foreign_key="role.id")


class Teacher(BaseSchema, TeacherBase, table=True):
    pass


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(TeacherBase):
    pass
