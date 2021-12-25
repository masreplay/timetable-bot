import os
from functools import lru_cache

from asc_scrapper.extract_asc_schedule import load_data
from asc_scrapper.schemas import *

dir_name = os.path.dirname(os.path.abspath('cards.json') + "/")


@lru_cache()
def get_cards():
    return load_data(dir_name + 'cards.json', Card)


@lru_cache()
def get_teachers():
    return load_data(dir_name + 'teachers.json', Teacher)


@lru_cache()
def get_lessons():
    return load_data(dir_name + 'lessons.json', Lesson)


@lru_cache()
def get_classrooms():
    return load_data(dir_name + 'classrooms.json', Classroom)


@lru_cache()
def get_periods():
    return load_data(dir_name + 'periods.json', Period)


@lru_cache()
def get_days_def():
    return load_data(dir_name + 'daysdefs.json', Day)


@lru_cache()
def get_subjects():
    return load_data(dir_name + 'subjects.json', Subject)


@lru_cache()
def get_classes():
    return load_data(dir_name + 'classes.json', Class)
