from typing import Optional, List
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import EmailStr, constr, validator
from pydantic.main import BaseModel
from sqlalchemy import Column, Enum
from sqlalchemy.orm import Query
from sqlmodel import Field

from app.core.utils.regex import url_regex
from app.core.utils.sql_alchemy_utils import sa_column_kwargs
from app.schemas.card_item import CardContent
from app.schemas.enums import UserGender, UserScrapeFrom

if TYPE_CHECKING:
    pass


# Shared properties
class UserBase(CardContent):
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


class JobTitle(BaseModel):
    id: UUID
    name: str


class OrmBase(BaseModel):
    # Common properties across orm models
    id: int

    # Pre-processing validator that evaluates lazy relationships before any other validation
    # NOTE: If high throughput/performance is a concern, you can/should probably apply
    #       this validator in a more targeted fashion instead of a wildcard in a base class.
    #       This approach is by no means slow, but adds a minor amount of overhead for every field
    @validator("*", pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, Query):
            return v.all()
        return v

    class Config:
        orm_mode = True


class User(UserBase, OrmBase):
    id: UUID
    job_titles: List[JobTitle]
