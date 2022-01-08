import os
from functools import lru_cache

from asc_scrapper import schemas
from asc_scrapper.extract_asc_schedule import load_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@lru_cache()
def get_cards():
    return load_data(os.path.join(BASE_DIR, 'cards.json'), schemas.Card)


@lru_cache()
def get_teachers():
    return load_data(os.path.join(BASE_DIR, 'teachers.json'), schemas.Teacher)


@lru_cache()
def get_lessons():
    return load_data(os.path.join(BASE_DIR, 'lessons.json'), schemas.Lesson)


@lru_cache()
def get_classrooms():
    return load_data(os.path.join(BASE_DIR, 'classrooms.json'), schemas.Classroom)


@lru_cache()
def get_classes():
    return load_data(os.path.join(BASE_DIR, 'classes.json.json'), schemas.Class)


@lru_cache()
def get_periods():
    return load_data(os.path.join(BASE_DIR, 'periods.json'), schemas.Period)


@lru_cache()
def get_buildings():
    return load_data(os.path.join(BASE_DIR, 'buildings.json'), schemas.Building)


@lru_cache()
def get_days_def():
    return load_data(os.path.join(BASE_DIR, 'daysdefs.json'), schemas.Day)


@lru_cache()
def get_subjects():
    return load_data(os.path.join(BASE_DIR, 'subjects.json'), schemas.Subject)



