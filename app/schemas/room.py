from typing import Optional
from uuid import UUID

from sqlalchemy import Enum, Column
from sqlmodel import Field

from app.schemas.card_item import CardContent
from app.schemas.enums import RoomType


# Shared properties
class RoomBase(CardContent):
    building_id: Optional[UUID] = Field(default=None, foreign_key="building.id")
    floor_id: Optional[UUID] = Field(default=None, foreign_key="floor.id")
    type: Optional[RoomType] = Field(sa_column=Column(Enum(RoomType)))


class Room(RoomBase):
    id: UUID
    pass


# Properties to receive via API on creation
class RoomCreate(RoomBase):
    pass


# Properties to receive via API on update
class RoomUpdate(RoomBase):
    pass
