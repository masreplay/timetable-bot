from typing import Optional

from pydantic import BaseModel, Field


class PermissionCrud(BaseModel):
    read: Optional[bool] = Field(True)
    create: Optional[bool] = Field(False)
    update: Optional[bool] = Field(False)
    delete: Optional[bool] = Field(False)


class Permission(BaseModel):
    user: PermissionCrud
    role: PermissionCrud


new_user_permission = Permission(
    user=PermissionCrud(),
    role=PermissionCrud(),
)
