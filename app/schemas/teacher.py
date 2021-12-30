from sqlmodel import SQLModel

from app.schemas.base_model import BaseSchema


class TeacherBase(SQLModel):
    name: str


class Teacher(BaseSchema, TeacherBase, table=True):
    pass


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(TeacherBase):
    pass
