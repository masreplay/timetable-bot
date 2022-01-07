from uuid import UUID

from app.schemas.card_item import CardContent
from app.schemas.location import Location


# Shared properties
class BuildingBase(CardContent, Location):
    pass


class Building(BuildingBase):
    id: UUID


# Properties to receive via API on creation
class BuildingCreate(BuildingBase):
    pass


# Properties to receive via API on update
class BuildingUpdate(BuildingBase):
    pass
