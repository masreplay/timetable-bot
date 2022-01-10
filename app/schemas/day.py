from uuid import UUID

from sqlmodel import SQLModel


# Shared properties
class DayBase(SQLModel):
    name: str


class Day(DayBase):
    id: UUID


# Properties to receive via API on creation
class DayCreate(DayBase):
    pass


# Properties to receive via API on update
class DayUpdate(DayBase):
    pass
