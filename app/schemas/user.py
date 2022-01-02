from typing import Optional
from uuid import UUID

from pydantic import EmailStr, constr
from sqlalchemy import Column, Enum
from sqlmodel import SQLModel, Field

from app.schemas.base import BaseSchema
from app.schemas.card_item import CardContent
from app.schemas.enums import UserType, UserGender, UserScrapeFrom
from app.utils.regex import url_regex
from app.utils.sql_alchemy_utils import sa_column_kwargs


class UserBase(CardContent):
    type: UserType = Field(default=None, sa_column=Column(Enum(UserType)))

    en_name: Optional[str] = Field(index=True)
    name: str = Field(index=True)
    email: Optional[EmailStr] = Field(default=None, sa_column_kwargs=sa_column_kwargs(unique=True))
    uot_url: Optional[constr(regex=url_regex)] = Field(default=None)
    image: Optional[constr(regex=url_regex)] = Field(default=None)

    gender: Optional[UserGender] = Field(sa_column=Column(Enum(UserGender)))

    # relations
    role_id: Optional[UUID] = Field(foreign_key="role.id")


class User(BaseSchema, UserBase, table=True):
    asc_job_title: Optional[str] = Field()
    asc_name: Optional[str] = Field()
    scrape_from: Optional[UserScrapeFrom] = Field(default=None, sa_column=Column(Enum(UserScrapeFrom)))


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass
