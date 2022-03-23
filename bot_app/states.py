from enum import Enum

from aiogram.dispatcher.filters.state import State, StatesGroup


class StageScheduleForm(StatesGroup):
    branch = State()
    stage = State()


class ScheduleTypeForm(StatesGroup):
    type = State()
    choose = State()


class ScheduleType(str, Enum):
    stages = "stages"
    teachers = "teachers"
    classrooms = "classrooms"
    subjects = "subjects"
