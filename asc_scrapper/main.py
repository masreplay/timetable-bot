from random import Random

import requests

from asc_scrapper.crud import get_schedule_by_class_name, get_periods, get_days
from asc_scrapper.schedule_html import schedule_html
from asc_scrapper.schemas import Schedule
from config import get_settings


def get_schedule_image(name: str):
    schedule: Schedule = get_schedule_by_class_name(name)
    url = get_settings().html_to_image_service

    data = schedule_html(periods=get_periods(), days=get_days(), cards=schedule)

    response = requests.get(url, data={"html": data}, stream=True)

    with open("table.g.html", "w", encoding="utf-8") as file:
        file.write(data)

    url = response.json()["url"]
    img_data = requests.get(url).content

    with open(f'{str(Random().randint(a=1, b=1000000))}table.png', 'wb') as handler:
        handler.write(img_data)
    return url


if __name__ == '__main__':
    get_schedule_image("ثالث برمجيات صباحي")

# matlab -38
# classroom_schedule("-38")
# class_schedule("*22")
# ولاء *58
# teacher_schedule("*24")
# print("\n".join([f"{teacher.short}, {teacher.id}" for teacher in get_teachers()]))
