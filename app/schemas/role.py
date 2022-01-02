from typing import Optional

from pydantic import Field
from sqlmodel import SQLModel

from app.schemas.base import BaseSchema
from app.utils.utils import Permission


class RoleBase(SQLModel):
    ar_name: str
    en_name: str


class Role(BaseSchema, RoleBase, table=True):
    permission: Optional[str] = Field(None)


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass
