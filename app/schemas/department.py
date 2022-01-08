
from uuid import UUID

from sqlmodel import SQLModel

from app.schemas.base import BaseSchema


class ClassBase(SQLModel):
    name: str
    en_name: str
    abbr: str | None
    vision: str | None


# Shared properties
class DepartmentBase(ClassBase):
    pass


class Department(BaseSchema, DepartmentBase):
    id: UUID


# Properties to receive via API on creation
class DepartmentCreate(DepartmentBase):
    pass


# Properties to receive via API on update
class DepartmentUpdate(DepartmentBase):
    pass
