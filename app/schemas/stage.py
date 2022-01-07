from typing import Optional
from uuid import UUID

from sqlalchemy import Column, Enum, UniqueConstraint
from sqlmodel import Field, SQLModel

from app.schemas.base import BaseSchema
from app.schemas.enums import CollageShifts


# Shared properties
class StageBase(SQLModel):
    __table_args__ = (UniqueConstraint('shift', 'level', 'branch_id', name='branch_stage'),)

    shift: Optional[CollageShifts] = Field(sa_column=Column(Enum(CollageShifts)))
    level: int = Field(ge=1, le=10)
    branch_id: Optional[UUID] = Field(default=None, foreign_key="branch.id")


class Stage(BaseSchema, StageBase):
    id: UUID


# Properties to receive via API on creation
class StageCreate(StageBase):
    pass


# Properties to receive via API on update
class StageUpdate(StageBase):
    pass
