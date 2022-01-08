from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import constr
from sqlmodel import SQLModel, Field

from app.core.utils.regex import color_regex


class BaseSchema(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # TODO: Add
    # updated_at: Optional[datetime] = Field(None)
    # updated_by: Optional[UUID] = Field(None)


class CardContent(SQLModel):
    name: Optional[str] = Field(index=True)
    color: constr(regex=color_regex)
