from pydantic.main import BaseModel
from sqlmodel import Field, SQLModel


class PermissionGroup(SQLModel):
    read: bool = Field(True)
    create: bool = Field(False)
    update: bool = Field(False)
    delete: bool = Field(False)


class Permissions(BaseModel):
    users: PermissionGroup
    roles: PermissionGroup
    periods: PermissionGroup
    job_titles: PermissionGroup
    departments: PermissionGroup
    branches: PermissionGroup
    stages: PermissionGroup


# default permissions for new role
default_permissions: Permissions = Permissions(
    users=PermissionGroup(),
    roles=PermissionGroup(
        read=False,
        create=False,
        update=False,
        delete=False,
    ),
    periods=PermissionGroup(),
    job_titles=PermissionGroup(),
    departments=PermissionGroup(),
    branches=PermissionGroup(),
    stages=PermissionGroup(),
)
