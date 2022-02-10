from typing import Any
from uuid import UUID

from pydantic import validator, BaseModel
from sqlmodel import SQLModel, Field

from app.schemas.card import CardBase
from app.schemas.day import DayBase
from app.schemas.floor import FloorBase
from app.schemas.lesson import LessonBase
from app.schemas.named_object import IdObject
from app.schemas.period import PeriodBase
from app.schemas.room import RoomBase
from app.schemas.stage import Stage
from app.schemas.subject import SubjectBase


class SubjectSchedule(SubjectBase):
    id: UUID


class DaySchedule(DayBase):
    id: UUID


class PeriodSchedule(PeriodBase):
    id: UUID

    @property
    def time(self) -> str:
        return f"{self.start_time.hour}:{self.start_time.minute} - {self.end_time.hour}:{self.end_time.minute}"


class LessonSchedule(LessonBase):
    id: UUID
    stages: list[IdObject]


class CardSchedule(CardBase):
    id: UUID


class BuildingSchedule(BaseModel):
    id: UUID
    name: str
    color: str


class ClassroomSchedule(RoomBase):
    id: UUID


class TeacherSchedule(BaseModel):
    id: UUID
    name: str
    color: str
    color_light: str


class FloorSchedule(FloorBase):
    id: UUID


class LessonScheduleSchemas(LessonBase):
    id: UUID
    stages: list

    @validator("stages", pre=True, check_fields=False, whole=True)
    def cast_stages(cls, value: Any):
        if len(value) > 0 and isinstance(value[0], dict):
            return [stage_id["id"] for stage_id in value]
        else:
            return value


class LessonScheduleDetails(LessonBase):
    id: UUID
    stages: list[Stage]
    teacher: TeacherSchedule | None
    subject: SubjectSchedule
    room: ClassroomSchedule | None


class CardScheduleDetails(CardBase):
    lesson: LessonScheduleDetails

    class Config:
        orm_mode = True


class ScheduleDetails(BaseModel):
    cards: list[CardScheduleDetails]
    days: list[DaySchedule]
    periods: list[PeriodSchedule]


# Generic will destroy the performance
class ScheduleBase(SQLModel):
    days: list[DaySchedule]
    periods: list[PeriodSchedule]

    cards: list[CardSchedule]

    buildings: list[BuildingSchedule]
    floors: list[FloorSchedule]
    classrooms: list[ClassroomSchedule]

    subjects: list[SubjectSchedule]
    teachers: list[TeacherSchedule]
    stages: list[Stage]


class Schedule(ScheduleBase):
    lessons: list[LessonSchedule]


class ScheduleSchemas(ScheduleBase):
    lessons: list[LessonScheduleSchemas]
