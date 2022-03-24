from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field
from sqlmodel import SQLModel


class TelegramUserBase(SQLModel):
    is_blocked: bool = Field(False)
    id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: str
    language_code: str


class TelegramChat(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    type: str


class TelegramEntity(BaseModel):
    type: str
    offset: int
    length: int


class TelegramModel(BaseModel):
    message_id: int
    from_: TelegramUserBase = Field(..., alias='from')
    chat: TelegramChat
    date: int
    text: str
    entities: List[TelegramEntity]
