from uuid import UUID

from pydantic import constr
from sqlmodel import SQLModel, Field

from app.core.utils import regex
from app.core.utils.sql_alchemy_utils import sa_column_kwargs
from app.schemas.permissions import Permissions


# Shared properties
class RoleBase(SQLModel):
    name: str = Field(..., sa_column_kwargs=sa_column_kwargs(unique=True))

    enum: constr(regex=regex.SCREAMING_SNAKE_CASE) | None = Field(
        default=None,
        sa_column_kwargs=sa_column_kwargs(unique=True),
    )
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
