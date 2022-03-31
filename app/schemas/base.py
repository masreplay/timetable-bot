from datetime import datetime
from uuid import UUID, uuid4

from pydantic import validator
from pydantic.color import Color
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, AutoString


class BaseSchema(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CardContent(SQLModel):
    name: str
    color: Color = Field(sa_column=Column(AutoString()))

    @validator("color")
    def color_as_hex(cls, v):
        return v.as_hex()
