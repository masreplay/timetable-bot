from datetime import time

from uuid import UUID

from sqlmodel import SQLModel


# Shared properties
class PeriodBase(SQLModel):
    name: str | None
    start_time: time
    end_time: time


class Period(PeriodBase):
    id: UUID


# Properties to receive via API on creation
class PeriodCreate(PeriodBase):
    pass


# Properties to receive via API on update
class PeriodUpdate(PeriodBase):
    pass
