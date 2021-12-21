from functools import lru_cache

from app.extract_asc_schedule import load_data
from schemas import *


@lru_cache()
def get_cards():
    return load_data('../test/cards.json', Card)


@lru_cache()
def get_teachers():
    return load_data('../test/teachers.json', Teacher)


@lru_cache()
def get_lessons():
    return load_data('../test/lessons.json', Lesson)


@lru_cache()
def get_classrooms():
    return load_data('../test/classrooms.json', Classroom)


@lru_cache()
def get_periods():
    return load_data('../test/periods.json', Period)


@lru_cache()
def get_days_def():
    return load_data('../test/daysdefs.json', Day)


@lru_cache()
def get_subjects():
    return load_data('../test/subjects.json', Subject)


@lru_cache()
def get_classes():
    return load_data('../test/classes.json', Class)
