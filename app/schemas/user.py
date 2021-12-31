from uuid import UUID
from enum import Enum
from typing import Optional

from pydantic import AnyHttpUrl, EmailStr
from sqlmodel import SQLModel, Field

from app.schemas.base_model import BaseSchema


class UserType(str, Enum):
    employee = "employee"
    teacher = "teacher"
    student = "student"
    other = "other"


class UserGender(str, Enum):
    male = "male"
    female = "female"


class UserBase(SQLModel):
    en_name: str = Field(index=True)
    ar_name: str = Field(index=True)
    email: Optional[EmailStr] = Field(default=None)
    uot_url: AnyHttpUrl = Field(default=None)
    image: AnyHttpUrl = Field(default=None)
    role_id: UUID = Field(foreign_key="role.id")


class User(BaseSchema, UserBase, table=True):
    pass


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass
