
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field


# Shared properties
class CardBase(SQLModel):
    __table_args__ = (UniqueConstraint('period_id', 'day_id', 'lesson_id', name='card_ids'),)
    period_id: UUID | None = Field(default=None, foreign_key="period.id")
    day_id: UUID = Field(default=None, foreign_key="day.id")
    lesson_id: UUID = Field(default=None, foreign_key="lesson.id")


class Card(CardBase):
    id: UUID
    pass


# Properties to receive via API on creation
class CardCreate(CardBase):
    pass


# Properties to receive via API on update
class CardUpdate(CardBase):
    pass
