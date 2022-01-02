from datetime import time
from typing import Optional

from sqlmodel import SQLModel

from app.schemas.base import BaseSchema


class PeriodBase(SQLModel):
    name: Optional[str]
    start_time: time
    end_time: time


class Period(PeriodBase, BaseSchema, table=True):
    pass


class PeriodCreate(PeriodBase):
    pass


class PeriodUpdate(PeriodBase):
    pass
