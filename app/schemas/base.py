from datetime import datetime
from uuid import UUID, uuid4

from pydantic import constr
from sqlmodel import SQLModel, Field

from app.core.utils.regex import color_regex
from bot_app.theme import random_dark, random_light


class BaseSchema(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # TODO: Add
    # updated_at: datetime | None = Field(None)
    # updated_by: UUID | None = Field(None)


class CardContent(SQLModel):
    name: str | None = Field(index=True)

    color: constr(regex=color_regex) | None
    color_light: constr(regex=color_regex) = Field(default_factory=random_light)
    color_dark: constr(regex=color_regex) = Field(default_factory=random_dark)
