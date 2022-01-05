from datetime import time
from typing import Optional

from sqlmodel import SQLModel

from app.schemas.base import BaseSchema

from sqlmodel import SQLModel


# Shared properties
class PeriodBase(SQLModel):
    name: Optional[str]
    start_time: time
    end_time: time


class Period(BaseSchema, PeriodBase, table=True):
    pass


# Properties to receive via API on creation
class PeriodCreate(PeriodBase):
    pass


# Properties to receive via API on update
class PeriodUpdate(PeriodBase):
    pass
