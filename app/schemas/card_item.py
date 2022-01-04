from typing import Optional

from pydantic import constr
from sqlmodel import SQLModel, Field

from app.core.utils.regex import color_regex


class CardContent(SQLModel):
    name: Optional[str] = Field(index=True)
    color: constr(regex=color_regex)
