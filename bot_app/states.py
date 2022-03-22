from aiogram.dispatcher.filters.state import State, StatesGroup


class StageScheduleForm(StatesGroup):
    branch = State()
    stage = State()


class Form(StatesGroup):
    teachers = State()
    classrooms = State()
    classes = State()
    subjects = State()
