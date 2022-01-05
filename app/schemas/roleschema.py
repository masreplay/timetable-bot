from typing import Union
from uuid import UUID

from pydantic import validator
from sqlmodel import Field, SQLModel, Column, JSON

from app.schemas.base import BaseSchema
from app.schemas.permissions import Permissions, default_permissions


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


# Additional properties stored in DB
class RoleSchema(BaseSchema, RoleBase, table=True):
    __tablename__ = "role"
    permissions: dict = Field(sa_column=Column(JSON), default_factory=default_permissions.dict)

    @validator('permissions', pre=True, always=True)
    def permissions_validate(cls, v: Union[dict, Permissions]):
        if isinstance(v, Permissions):
            return v.dict()
        elif isinstance(v, dict):
            v = Permissions(**v)
            return v.dict()
        raise ValueError(v)

    @property
    def permissions_(self):
        return Permissions(**self.permissions)
