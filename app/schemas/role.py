from sqlmodel import SQLModel

from app.schemas.base_model import BaseSchema


class RoleBase(SQLModel):
    name: str


class Role(BaseSchema, RoleBase, table=True):
    pass


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass
