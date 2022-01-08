import os
from functools import lru_cache
from typing import List

from asc_scrapper.extract_asc_schedule import load_data
from uot_scraper.schemas import Teacher, Role

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@lru_cache()
def get_teachers() -> List[Teacher]:
    return load_data(os.path.join(BASE_DIR, 'cs_teachers.json'), Teacher, data_rows="results")


@lru_cache()
def get_roles() -> List[Role]:
    return load_data(os.path.join(BASE_DIR, 'cs_roles.json'), Role, data_rows="results")
