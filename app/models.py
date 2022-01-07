from typing import List, Optional, Union
from uuid import UUID

from pydantic import validator
from sqlmodel import Relationship, SQLModel, Field, Column, JSON

from app.schemas.base import BaseSchema
from app.schemas.branch import BranchBase
from app.schemas.department import DepartmentBase
from app.schemas.job_title import JobTitleBase
from app.schemas.period import PeriodBase
from app.schemas.permissions import default_permissions, Permissions
from app.schemas.role import RoleBase
from app.schemas.stage import StageBase
from app.schemas.user import UserBase


class UserJobTitle(SQLModel, table=True):
    __tablename__ = "user_job_title"
    __name__ = "user_job_title"
    job_title_id: Optional[UUID] = Field(
        default=None, foreign_key="job_title.id", primary_key=True
    )
    user_id: Optional[UUID] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )


class JobTitle(BaseSchema, JobTitleBase, table=True):
    __tablename__ = "job_title"
    __name__ = "job_title"
    users: List["User"] = Relationship(back_populates="job_titles", link_model=UserJobTitle)


class User(UserBase, BaseSchema, table=True):
    job_titles: List["JobTitle"] = Relationship(back_populates="users", link_model=UserJobTitle)
    hashed_password: Optional[str] = Field(None)

    class Config:
        orm_mode = True


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


class Period(BaseSchema, PeriodBase, table=True):
    pass


class Department(BaseSchema, DepartmentBase, table=True):
    branches: List["Branch"] = Relationship(back_populates="department")


class Branch(BaseSchema, BranchBase, table=True):
    department: "Department" = Relationship(back_populates="branches")
    stages: List["Stage"] = Relationship(back_populates="branch")


class Stage(BaseSchema, StageBase, table=True):
    branch: "Branch" = Relationship(back_populates="stages")
