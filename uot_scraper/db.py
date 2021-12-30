import os
from functools import lru_cache
from typing import List

from asc_scrapper.extract_asc_schedule import load_data
from uot_scraper.schemas import UotTeacher, UotRole

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@lru_cache()
def get_teachers() -> List[UotTeacher]:
    return load_data(os.path.join(BASE_DIR, 'cs_teachers.json'), UotTeacher, data_rows="results")


@lru_cache()
def get_roles() -> List[UotRole]:
    return load_data(os.path.join(BASE_DIR, 'cs_roles.json'), UotRole, data_rows="results")
