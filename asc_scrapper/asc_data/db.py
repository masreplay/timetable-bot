import os
from functools import lru_cache

from asc_scrapper.extract_asc_schedule import load_data
from asc_scrapper.schemas import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@lru_cache()
def get_cards():
    return load_data(os.path.join(BASE_DIR, 'cards.json'), AscCard)


@lru_cache()
def get_teachers():
    return load_data(os.path.join(BASE_DIR, 'teachers.json'), AscTeacher)


@lru_cache()
def get_lessons():
    return load_data(os.path.join(BASE_DIR, 'lessons.json'), AscLesson)


@lru_cache()
def get_classrooms():
    return load_data(os.path.join(BASE_DIR, 'classrooms.json'), AscClassroom)


@lru_cache()
def get_periods():
    return load_data(os.path.join(BASE_DIR, 'periods.json'), AscPeriod)


@lru_cache()
def get_days_def():
    return load_data(os.path.join(BASE_DIR, 'daysdefs.json'), AscDay)


@lru_cache()
def get_subjects():
    return load_data(os.path.join(BASE_DIR, 'subjects.json'), AscSubject)


@lru_cache()
def get_classes():
    return load_data(os.path.join(BASE_DIR, 'classes.json'), AscClass)
