from uuid import UUID
from enum import Enum
from typing import Optional

from pydantic import AnyHttpUrl, EmailStr
from pydantic.color import Color
from sqlmodel import SQLModel, Field

from app.schemas.base_model import BaseSchema


class UserType(str, Enum):
    employee = "employee"
    teacher = "teacher"

    # teacher and employee
    teacher_employee = "teacher_employee"

    student = "student"
    other = "other"


class UserGender(str, Enum):
    male = "male"
    female = "female"


class UserScrapeFrom(str, Enum):
    # https://cs.uotechnology.edu.iq/index.php/s/cv/
    uot = "uot"
    # https://uotcs.edupage.org/timetable/
    asc = "asc"
    # both of them
    uot_asc = "uot_asc"


class UserBase(SQLModel):
    type: UserType

    # uot
    en_name: Optional[str] = Field(index=True)
    ar_name: Optional[str] = Field(index=True)
    email: Optional[EmailStr] = Field(default=None)
    uot_url: Optional[AnyHttpUrl] = Field(default=None)
    image: Optional[AnyHttpUrl] = Field(default=None)

    # asc
    color: Color = Field()
    asc_job_title: str = Field()
    asc_name: str = Field()
    scrape_from: Optional[UserScrapeFrom] = Field(default=None)
    gender: UserGender = Field()

    # relations
    role_id: Optional[UUID] = Field(foreign_key="role.id")


class User(BaseSchema, UserBase, table=True):
    pass


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass
