import json
import pathlib

import requests

from app.core.config import settings
from scrapers.asc_scrapper.crud import AscCRUD
from scrapers.asc_scrapper.schedule_html import schedule_html

IMAGE_URL = f"{settings().HTML_TO_IMAGE_SERVICE}/image"


def get_schedule_image(name: str, test: bool = True) -> str | None:
    json_file = open("/asc_schedule.json", encoding="utf8")
    data = json.load(json_file)
    asc_crud: AscCRUD = AscCRUD(data=data)

    periods = asc_crud.get_periods()
    days = asc_crud.get_days()

    schedule = asc_crud.get_class_schedule_by_name(name)

    data = schedule_html(periods=periods, days=days, cards=schedule, title=name, is_dark=True)

    response = requests.post(IMAGE_URL, data={"html": data}, stream=True)
    image_url = ImageUrl.parse_obj(response.json())

    img_data = requests.get(image_url.url).content

    pathlib.Path("generated_data").mkdir(parents=True, exist_ok=True)
    with open(f'generated_data/{name}table.png', 'wb') as handler:
        handler.write(img_data)
    if test:
        with open("generated_data/table.g.html", "w", encoding="utf-8") as file:
            file.write(data)

    return image_url.url


if __name__ == '__main__':
    get_schedule_image("ثالث برمجيات صباحي", test=True)
