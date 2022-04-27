from uuid import UUID

from pydantic import EmailStr, constr, validator
from pydantic.main import BaseModel
from sqlalchemy import Column, Enum
from sqlmodel import Field

from app.core.as_form_data import as_form
from app.core.utils.fix_form_data import form_data_to_list
from app.core.utils.regex import URL_REGEX
from app.core.utils.sql_alchemy_utils import sa_column_kwargs
from app.schemas import ScheduleDetails
from app.schemas.base import CardContent
from app.schemas.enums import UserGender, UserScrapeFrom


# Shared properties


class UserBase(CardContent):
    email: EmailStr | None = Field(default=None, sa_column_kwargs=sa_column_kwargs(unique=True))
    uot_url: constr(regex=URL_REGEX) | None = Field(default=None)
    image_url: constr(regex=URL_REGEX) | None = Field(default=None)
    is_active: bool | None = True

    gender: UserGender | None = Field(sa_column=Column(Enum(UserGender)))

    asc_job_title: str | None = Field()
    asc_name: str | None = Field()
    scrape_from: UserScrapeFrom | None = Field(
        default=None, sa_column=Column(Enum(UserScrapeFrom)))

    # relations
    role_id: UUID = Field(foreign_key="role.id")


class UserCreateDB(UserBase):
    password: str | None = Field(None, min_length=8, max_length=16)


# Properties to receive via API on creation
@as_form
class UserCreate(CardContent):
    email: EmailStr | None = Field(default=None, sa_column_kwargs=sa_column_kwargs(unique=True))
    password: str | None = Field(None, min_length=8, max_length=16)
    uot_url: constr(regex=URL_REGEX) | None = Field(default=None)
    gender: UserGender | None = Field(sa_column=Column(Enum(UserGender)))
    role_id: UUID
    job_titles: list[str] = Field([])

    @validator("job_titles")
    def fix_job_titles(cls, v): return form_data_to_list(v, UUID)


# Properties to receive via API on update
@as_form
class UserUpdate(CardContent):
    email: EmailStr | None = Field(default=None, sa_column_kwargs=sa_column_kwargs(unique=True))
    password: str | None = Field(None, min_length=8, max_length=16)
    uot_url: constr(regex=URL_REGEX) | None = Field(default=None)
    gender: UserGender | None = Field(sa_column=Column(Enum(UserGender)))
    role_id: UUID


class JobTitle(BaseModel):
    id: UUID
    name: str


class User(UserBase):
    id: UUID
    job_titles: list[JobTitle]


class UserDetails(UserBase):
    id: UUID
    job_titles: list[JobTitle]
    schedule: ScheduleDetails | None
