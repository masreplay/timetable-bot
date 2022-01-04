from pydantic import BaseModel
from pydantic.utils import GetterDict


class PermissionCRUD(BaseModel):
    read: bool
    create: bool
    update: bool
    delete: bool


class Permissions(BaseModel):
    users: PermissionCRUD
    roles: PermissionCRUD

    class Config:
        getter_dict = GetterDict


# default permissions for new role
default_permissions: Permissions = Permissions(
    users=PermissionCRUD(
        read=True,
        create=False,
        update=False,
        delete=False,
    ),
    roles=PermissionCRUD(
        read=False,
        create=False,
        update=False,
        delete=False,
    ),
)


