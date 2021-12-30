from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class BaseSchema(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)
