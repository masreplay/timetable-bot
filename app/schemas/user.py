from uuid import UUID

from pydantic import EmailStr, constr
from pydantic.main import BaseModel
from sqlalchemy import Column, Enum
from sqlmodel import Field

from app.core.utils.regex import url_regex, color_regex
from app.core.utils.sql_alchemy_utils import sa_column_kwargs
from app.schemas.base import CardContent
from app.schemas.enums import UserGender, UserScrapeFrom


# Shared properties
class UserBase(CardContent):
    en_name: str | None = Field(index=True)
    email: EmailStr | None = Field(
        default=None, sa_column_kwargs=sa_column_kwargs(unique=True))
    uot_url: constr(regex=url_regex) | None = Field(default=None)
    image: constr(regex=url_regex) | None = Field(default=None)
    is_active: bool | None = True

    gender: UserGender | None = Field(sa_column=Column(Enum(UserGender)))

    asc_job_title: str | None = Field()
    asc_name: str | None = Field()
    scrape_from: UserScrapeFrom | None = Field(
        default=None, sa_column=Column(Enum(UserScrapeFrom)))

    # relations
    role_id: UUID | None = Field(foreign_key="role.id")


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str | None = Field(None, min_length=8, max_length=16)

# Properties to receive via API on update


class UserUpdate(UserBase):
    password: str | None = Field(None, min_length=8, max_length=16)


class JobTitle(BaseModel):
    id: UUID
    name: str


class User(UserBase):
    id: UUID
    job_titles: list[JobTitle]
