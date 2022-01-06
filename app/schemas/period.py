from datetime import time
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel


# Shared properties
class PeriodBase(SQLModel):
    name: Optional[str]
    start_time: time
    end_time: time


# Properties to receive via API on creation
class PeriodCreate(PeriodBase):
    pass


# Properties to receive via API on update
class PeriodUpdate(PeriodBase):
    pass


class Period(PeriodBase):
    id: UUID
