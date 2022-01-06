from uuid import UUID

from sqlmodel import SQLModel

from app.schemas.permissions import Permissions


# Shared properties
class RoleBase(SQLModel):
    ar_name: str
    en_name: str
    permissions: Permissions


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    pass


# Properties to receive via API on update
class RoleUpdate(RoleBase):
    pass


# Properties to return via API
class Role(RoleBase):
    id: UUID
