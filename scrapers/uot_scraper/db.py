import json
import os
from functools import lru_cache
from typing import TypeVar, Type

from pydantic import parse_obj_as

from scrapers.uot_scraper.schemas import Teacher, Role

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

T = TypeVar("T")


def parse_json_list(file_dir: str, type_: Type[T], data="results") -> list[T]:
    """
    parse json have list data filed {"data": []}
    :param file_dir:
    :param type_:
    :param data:
    :return:
    """
    with open(file_dir, "r", encoding='utf-8') as f:
        json_list = json.load(f)
        return parse_obj_as(list[type_], json_list[data])


@lru_cache()
def get_teachers() -> list[Teacher]:
    return parse_json_list(os.path.join(BASE_DIR, '../../data/cs_teachers.json'), Teacher, data="results")


@lru_cache()
def get_roles() -> list[Role]:
    return parse_json_list(os.path.join(BASE_DIR, '../../data/cs_roles.json'), Role, data="results")
