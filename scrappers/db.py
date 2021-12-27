import os
from functools import lru_cache

from asc_scrapper.extract_asc_schedule import load_data
from scrappers.schemas import UotTeacher

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@lru_cache()
def get_teachers():
    return load_data(os.path.join(BASE_DIR, 'cs_teachers.json'), UotTeacher, data_rows="results")
