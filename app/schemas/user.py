from typing import Optional
from uuid import UUID

from pydantic import EmailStr, constr
from sqlalchemy import Column, Enum
from sqlmodel import Field

from app.core.utils.regex import url_regex
from app.core.utils.sql_alchemy_utils import sa_column_kwargs
from app.schemas.base import BaseSchema
from app.schemas.card_item import CardContent
from app.schemas.enums import UserType, UserGender, UserScrapeFrom


# Shared properties
class UserBase(CardContent):
    type: UserType = Field(default=None, sa_column=Column(Enum(UserType)))

    en_name: Optional[str] = Field(index=True)
    email: Optional[EmailStr] = Field(default=None, sa_column_kwargs=sa_column_kwargs(unique=True))
    uot_url: Optional[constr(regex=url_regex)] = Field(default=None)
    image: Optional[constr(regex=url_regex)] = Field(default=None)

    is_active: Optional[bool] = True

    gender: Optional[UserGender] = Field(sa_column=Column(Enum(UserGender)))

    asc_job_title: Optional[str] = Field()
    asc_name: Optional[str] = Field()
    scrape_from: Optional[UserScrapeFrom] = Field(default=None, sa_column=Column(Enum(UserScrapeFrom)))

    # relations
    role_id: Optional[UUID] = Field(foreign_key="role.id")


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: Optional[str] = Field(None, min_length=8, max_length=16)


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8, max_length=16)


# Properties to return via API
class User(UserBase):
    id: UUID


# Additional properties stored in DB
class UserSchema(UserBase, BaseSchema, table=True):
    __tablename__ = "user"
    hashed_password: Optional[str]
