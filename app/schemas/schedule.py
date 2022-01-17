from typing import Any, List
from uuid import UUID

from pydantic import validator, root_validator
from sqlmodel import SQLModel

from app.schemas.building import BuildingBase
from app.schemas.card import CardBase
from app.schemas.day import DayBase
from app.schemas.floor import FloorBase
from app.schemas.lesson import LessonBase
from app.schemas.named_object import IdObject
from app.schemas.period import PeriodBase
from app.schemas.room import RoomBase
from app.schemas.stage import StageSchedule
from app.schemas.subject import SubjectBase
from app.schemas.user import UserBase


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


class BuildingSchedule(BuildingBase):
    id: UUID


class ClassroomSchedule(RoomBase):
    id: UUID


class TeacherSchedule(UserBase):
    id: UUID


class FloorSchedule(FloorBase):
    id: UUID


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
    stages: list[StageSchedule]


class LessonScheduleSchemas(LessonBase):
    id: UUID
    stages: list

    @validator("stages", pre=True, check_fields=False, whole=True)
    def cast_stages(cls, value: Any):
        if len(value) > 0 and isinstance(value[0], dict):
            return [stage_id["id"] for stage_id in value]
        else:
            return value


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
    stages: list[StageSchedule]
