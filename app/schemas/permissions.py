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
    days: PermissionGroup
    stages: PermissionGroup
    buildings: PermissionGroup
    rooms: PermissionGroup
    floors: PermissionGroup
    subjects: PermissionGroup
    lessons: PermissionGroup
    cards: PermissionGroup


# default permissions for new role
default_permissions: Permissions = Permissions(
    users=PermissionGroup(),
    roles=PermissionGroup(read=False, create=False, update=False, delete=False),
    periods=PermissionGroup(),
    job_titles=PermissionGroup(),
    departments=PermissionGroup(),
    branches=PermissionGroup(),
    stages=PermissionGroup(),
    buildings=PermissionGroup(),
    rooms=PermissionGroup(),
    floors=PermissionGroup(),
    subjects=PermissionGroup(),
    lessons=PermissionGroup(),
    cards=PermissionGroup(),
    days=PermissionGroup(),
)

full_crud_permission = PermissionGroup(
    create=True,
    read=True,
    update=True,
    delete=True,
)

super_admin_permissions: Permissions = Permissions(
    users=full_crud_permission,
    roles=full_crud_permission,
    periods=full_crud_permission,
    job_titles=full_crud_permission,
    departments=full_crud_permission,
    branches=full_crud_permission,
    stages=full_crud_permission,
    buildings=full_crud_permission,
    rooms=full_crud_permission,
    floors=full_crud_permission,
    subjects=full_crud_permission,
    lessons=full_crud_permission,
    cards=full_crud_permission,
    days=full_crud_permission,
)
