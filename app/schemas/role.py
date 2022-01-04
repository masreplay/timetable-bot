from sqlmodel import Field, SQLModel, Column, JSON
from pydantic import json
from app.schemas.base import BaseSchema
from app.schemas.permission import new_user_permission, PermissionCrud


class RoleBase(SQLModel):
    ar_name: str
    en_name: str
    permissions: PermissionCrud = Field(sa_column=Column(JSON), default=new_user_permission.json())


class Role(BaseSchema, RoleBase, table=True):
    pass

    class Config:
        orm_mode = True


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass
