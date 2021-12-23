from functools import lru_cache

from app.extract_asc_schedule import load_data
from app.schemas import *


@lru_cache()
def get_cards():
    return load_data('../data/cards.json', Card)


@lru_cache()
def get_teachers():
    return load_data('../data/teachers.json', Teacher)


@lru_cache()
def get_lessons():
    return load_data('../data/lessons.json', Lesson)


@lru_cache()
def get_classrooms():
    return load_data('../data/classrooms.json', Classroom)


@lru_cache()
def get_periods():
    return load_data('../data/periods.json', Period)


@lru_cache()
def get_days_def():
    return load_data('../data/daysdefs.json', Day)


@lru_cache()
def get_subjects():
    return load_data('../data/subjects.json', Subject)


@lru_cache()
def get_classes():
    return load_data('../data/classes.json', Class)
