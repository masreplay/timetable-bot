from pydantic import BaseModel
from pydantic.utils import GetterDict
from sqlmodel import Field


class PermissionGroup(BaseModel):
    read: bool = Field(True)
    create: bool = Field(False)
    update: bool = Field(False)
    delete: bool = Field(False)


class Permissions(BaseModel):
    users: PermissionGroup
    roles: PermissionGroup
    periods: PermissionGroup

    class Config:
        getter_dict = GetterDict


# default permissions for new role
default_permissions: Permissions = Permissions(
    users=PermissionGroup(),
    roles=PermissionGroup(
        read=False,
        create=False,
        update=False,
        delete=False,
    ),
    periods=PermissionGroup()
)
