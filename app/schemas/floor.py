from uuid import UUID

from sqlmodel import SQLModel


# Shared properties
class FloorBase(SQLModel):
    pass
    # TODO
    # name: str
    # number: int


class Floor(FloorBase):
    id: UUID


# Properties to receive via API on creation
class FloorCreate(FloorBase):
    pass


# Properties to receive via API on update
class FloorUpdate(FloorBase):
    pass
