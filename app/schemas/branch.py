from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from app.schemas.department import ClassBase
from app.schemas.base import BaseSchema


# Shared properties
class BranchBase(ClassBase):
    department_id: UUID = Field(default=None, foreign_key="department.id")


class Branch(BaseSchema, BranchBase):
    id: UUID


# Properties to receive via API on creation
class BranchCreate(BranchBase):
    pass


# Properties to receive via API on update
class BranchUpdate(BranchBase):
    pass
