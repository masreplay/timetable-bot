from uuid import UUID

from sqlalchemy import Enum, Column
from sqlmodel import Field

from app.schemas.base import CardContent
from app.schemas.enums import RoomType


# Shared properties
class RoomBase(CardContent):
    building_id: UUID | None = Field(default=None, foreign_key="building.id")
    floor_id: UUID | None = Field(default=None, foreign_key="floor.id")
    type: RoomType | None = Field(sa_column=Column(Enum(RoomType)))


class Room(RoomBase):
    id: UUID


# Properties to receive via API on creation
class RoomCreate(RoomBase):
    pass


# Properties to receive via API on update
class RoomUpdate(RoomBase):
    pass
