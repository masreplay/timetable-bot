
from uuid import UUID

from sqlmodel import SQLModel

# Shared properties
from app.schemas.enums import UserType


class JobTitleBase(SQLModel):
    name: str
    en_name: str | None
    type: UserType


# Properties to receive via API on creation
class JobTitleCreate(JobTitleBase):
    pass


# Properties to receive via API on update
class JobTitleUpdate(JobTitleBase):
    pass


class JobTitle(JobTitleBase):
    id: UUID
