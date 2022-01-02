from pydantic import constr
from sqlmodel import SQLModel

from app.utils.regex import color_regex


class CardContent(SQLModel):
    name: str
    color: constr(regex=color_regex)
