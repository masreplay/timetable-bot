from uuid import UUID

from pydantic import root_validator
from sqlalchemy import Column, Enum
from sqlmodel import Field, SQLModel

from app.schemas import enums
from app.schemas.enums import CollageShifts
from app.schemas.named_object import NamedObject


# Shared properties
class StageBase(SQLModel):
    # __table_args__ = (UniqueConstraint('shift', 'level', 'branch_id', name='branch_stage'),)
    name: str
    shift: CollageShifts | None = Field(index=True, sa_column=Column(Enum(CollageShifts)))
    level: int | None = Field(index=True, ge=1, le=10)
    branch_id: UUID | None = Field(default=None, foreign_key="branch.id")


class Branch(NamedObject):
    department: NamedObject

    class Config:
        orm_mode = True


stage_level_t = {
    1: "أول",
    2: "ثاني",
    3: "ثالث",
    4: "رابع",
    5: "خامس",
}

stage_shift_t = {
    enums.CollageShifts.morning: "صباحي",
    enums.CollageShifts.evening: "مسائي",
}


class StageScheduleDetails(StageBase):
    id: UUID
    branch: NamedObject

    class Config:
        orm_mode = True


class Stage(StageBase):
    id: UUID
    name: str
    branch: Branch

    # @root_validator(pre=True)
    # def name_reshape(cls, values):
    #     if values['name']:
    #         return values
    #     else:
    #         new: dict = dict(values)
    #         level: str = stage_level_t[new.get('level')]
    #         shift: str = stage_shift_t[new.get('shift')]
    #         branch: Branch = new.get('branch')
    #         new['name'] = f"{level} {branch.name} {shift}"
    #         return new

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class StageCreate(StageBase):
    pass


# Properties to receive via API on update
class StageUpdate(StageBase):
    pass
