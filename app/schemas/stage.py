from uuid import UUID

from sqlalchemy import Column, Enum, UniqueConstraint
from sqlmodel import Field, SQLModel

from app.schemas.enums import CollageShifts
from app.schemas.named_object import NamedObject


# Shared properties
class StageBase(SQLModel):
    __table_args__ = (UniqueConstraint('shift', 'level', 'branch_id', name='branch_stage'),)

    shift: CollageShifts | None = Field(index=True, sa_column=Column(Enum(CollageShifts)))
    level: int = Field(index=True, ge=1, le=10)
    branch_id: UUID | None = Field(default=None, foreign_key="branch.id")


class Branch(NamedObject):
    department: NamedObject

    class Config:
        orm_mode = True


class Stage(StageBase):
    id: UUID
    branch: Branch


# Properties to receive via API on creation
class StageCreate(StageBase):
    pass


# Properties to receive via API on update
class StageUpdate(StageBase):
    pass
