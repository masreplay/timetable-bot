import json
import pathlib

import requests

from app.core.config import settings
from asc_scrapper.crud import AscCRUD
from asc_scrapper.schedule_html import schedule_html
from asc_scrapper.schemas import Schedule

IMAGE_URL = settings().HTML_TO_IMAGE_SERVICE + "image"


def get_schedule_image(name: str, test: bool = True):
    json_file = open("../asc_scrapper/asc_schedule.json", encoding="utf8")
    data = json.load(json_file)
    asc_crud: AscCRUD = AscCRUD(data=data)

    periods = asc_crud.get_periods()
    days = asc_crud.get_days()

    schedule: Schedule = asc_crud.get_schedule_by_class_name(name)

    data = schedule_html(periods=periods, days=days, cards=schedule, title=name, is_dark=True)

    response = requests.get(IMAGE_URL, data={"html": data}, stream=True)
    url = response.json()["url"]
    img_data = requests.get(url).content
    pathlib.Path("generated_data").mkdir(parents=True, exist_ok=True)
    with open(f'generated_data/{name}table.png', 'wb') as handler:
        handler.write(img_data)
    if test:
        with open("generated_data/table.g.html", "w", encoding="utf-8") as file:
            file.write(data)

    return url


if __name__ == '__main__':
    get_schedule_image("ثالث برمجيات صباحي", test=True)
