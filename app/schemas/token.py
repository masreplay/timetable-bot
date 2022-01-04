from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenPayload(SQLModel):
    sub: Optional[UUID] = None
