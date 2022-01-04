from typing import Union

from pydantic import validator
from sqlmodel import Field, SQLModel, Column, JSON

from app.schemas.base import BaseSchema
from app.schemas.permissions import Permissions, default_permissions


class RoleBase(SQLModel):
    ar_name: str
    en_name: str
    permissions: Permissions


class Role(BaseSchema, RoleBase, table=True):
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


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass
