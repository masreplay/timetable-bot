from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field


class BaseSchema(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # TODO: Add
    # updated_at: Optional[datetime] = Field(None)
    # updated_by: Optional[UUID] = Field(None)
