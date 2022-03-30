from datetime import datetime
from uuid import UUID, uuid4

from pydantic import constr
from sqlmodel import SQLModel, Field

from app.core.utils.regex import color_regex
from ui.colors.generate_color import random_light, random_dark


class BaseSchema(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CardContent(SQLModel):
    name: str | None = Field(index=True)
    color: constr(regex=color_regex) | None
