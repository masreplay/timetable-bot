from typing import Any
from uuid import UUID

from pydantic import validator
from sqlmodel import SQLModel

from app import models
from app.schemas.building import BuildingBase
from app.schemas.card import CardBase
from app.schemas.day import DayBase
from app.schemas.floor import FloorBase
from app.schemas.lesson import LessonBase
from app.schemas.named_object import NamedObject, IdObject
from app.schemas.period import PeriodBase
from app.schemas.room import RoomBase
from app.schemas.stage import StageBase, Stage, StageSchedule
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
