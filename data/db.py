import os
from functools import lru_cache

from asc_scrapper.extract_asc_schedule import load_data
from asc_scrapper.schemas import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'


@lru_cache()
def get_cards():
    return load_data(os.path.join(BASE_DIR, 'cards.json'), Card)


@lru_cache()
def get_teachers():
    return load_data(os.path.dirname(os.path.abspath('teachers.json')), Teacher)


@lru_cache()
def get_lessons():
    return load_data(os.path.dirname(os.path.abspath('lessons.json')), Lesson)


@lru_cache()
def get_classrooms():
    return load_data(os.path.dirname(os.path.abspath('classrooms.json')), Classroom)


@lru_cache()
def get_periods():
    return load_data(os.path.dirname(os.path.abspath('periods.json')), Period)


@lru_cache()
def get_days_def():
    return load_data(os.path.dirname(os.path.abspath('daysdefs.json')), Day)


@lru_cache()
def get_subjects():
    return load_data(os.path.dirname(os.path.abspath('subjects.json')), Subject)


@lru_cache()
def get_classes():
    return load_data(os.path.dirname(os.path.abspath('classes.json')), Class)
