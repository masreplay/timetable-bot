from typing import Optional
from uuid import UUID

from pydantic import EmailStr, BaseModel, constr
from sqlalchemy import Column, Enum, UniqueConstraint
from sqlmodel import SQLModel, Field

from app.schemas.base_model import BaseSchema
from app.schemas.enums import UserType, UserGender, UserScrapeFrom

url_regex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
color_regex = r'^#(?:[0-9a-fA-F]{3}){1,2}$'


class Short(SQLModel):
    pass


class SaColumnKwargs(BaseModel):
    unique: bool


class UserBase(SQLModel):
    type: UserType = Field(default=None, sa_column=Column(Enum(UserType)))

    en_name: Optional[str] = Field(index=True)
    ar_name: str = Field(index=True)
    email: Optional[EmailStr] = Field(default=None, sa_column_kwargs=SaColumnKwargs(unique=True).dict())
    uot_url: Optional[constr(regex=url_regex)] = Field(default=None)
    image: Optional[constr(regex=url_regex)] = Field(default=None)

    color: constr(regex=color_regex)
    gender: Optional[UserGender] = Field(sa_column=Column(Enum(UserGender)))

    # relations
    role_id: Optional[UUID] = Field(foreign_key="role.id")


class User(BaseSchema, UserBase, Short, table=True):
    asc_job_title: Optional[str] = Field()
    asc_name: Optional[str] = Field()
    scrape_from: Optional[UserScrapeFrom] = Field(default=None, sa_column=Column(Enum(UserScrapeFrom)))


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass
