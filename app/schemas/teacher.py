from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Teacher(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # TODO Fix default None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)
    name: str


class TeacherCreate(SQLModel):
    name: str
