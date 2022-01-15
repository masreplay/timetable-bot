from uuid import UUID

from sqlalchemy import Column, Enum
from sqlmodel import SQLModel, Field

# Shared properties
from app.schemas.enums import UserType


class JobTitleBase(SQLModel):
    name: str
    en_name: str | None
    type: UserType | None = Field(sa_column=Column(Enum(UserType)))


# Properties to receive via API on creation
class JobTitleCreate(JobTitleBase):
    pass


# Properties to receive via API on update
class JobTitleUpdate(JobTitleBase):
    pass


class JobTitle(JobTitleBase):
    id: UUID
