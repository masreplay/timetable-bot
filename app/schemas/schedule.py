from datetime import date
from typing import Any, Optional
from typing import TypeVar, Generic
from uuid import UUID

from pydantic import validator, BaseModel
from pydantic.generics import GenericModel
from sqlmodel import SQLModel

from app.schemas.base import CardContent
from app.schemas.card import CardBase
from app.schemas.day import DayBase
from app.schemas.floor import FloorBase
from app.schemas.lesson import LessonBase
from app.schemas.named_object import IdObject
from app.schemas.period import PeriodBase
from app.schemas.rights import Rights
from app.schemas.room import RoomBase
from app.schemas.schedule_information import ScheduleInformation
from app.schemas.stage import Stage
from app.schemas.subject import SubjectBase
from bot_app.states import ScheduleType

ModelType = TypeVar('ModelType')


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


class TeacherSchedule(CardContent):
    id: UUID


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


class ScheduleDetailsItem(BaseModel):
    id: UUID
    name: str | None = None
    type: ScheduleType


class ScheduleDetails(BaseModel):
    item: ScheduleDetailsItem
    cards: list[CardScheduleDetails]
    days: list[DaySchedule]
    periods: list[PeriodSchedule]


# Don't use Generic will destroy the performance
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
