from typing import Any
from uuid import UUID

from pydantic import validator, BaseModel
from sqlmodel import SQLModel

from app.schemas.card import CardBase
from app.schemas.day import DayBase
from app.schemas.floor import FloorBase
from app.schemas.lesson import LessonBase
from app.schemas.named_object import IdObject
from app.schemas.period import PeriodBase
from app.schemas.room import RoomBase
from app.schemas.stage import StageScheduleDetails, Stage, StageBase
from app.schemas.subject import SubjectBase


class SubjectSchedule(SubjectBase):
    id: UUID


class DaySchedule(DayBase):
    id: UUID


class PeriodSchedule(PeriodBase):
    id: UUID


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


class ScheduleCard(CardBase):
    lesson: LessonScheduleDetails

    class Config:
        orm_mode = True


# Generic will destroy the performance


class Schedule(SQLModel):
    days: list[DaySchedule]
    periods: list[PeriodSchedule]

    cards: list[CardSchedule]
    lessons: list[LessonSchedule]

    buildings: list[BuildingSchedule]
    floors: list[FloorSchedule]
    classrooms: list[ClassroomSchedule]

    subjects: list[SubjectSchedule]
    teachers: list[TeacherSchedule]
    stages: list[Stage]


class ScheduleSchemas(SQLModel):
    days: list[DaySchedule]
    periods: list[PeriodSchedule]

    cards: list[CardSchedule]
    lessons: list[LessonScheduleSchemas]

    buildings: list[BuildingSchedule]
    floors: list[FloorSchedule]
    classrooms: list[ClassroomSchedule]

    subjects: list[SubjectSchedule]
    teachers: list[TeacherSchedule]
    stages: list[Stage]
