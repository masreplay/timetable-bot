from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class BaseSchema(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    # TODO Fix default None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)
