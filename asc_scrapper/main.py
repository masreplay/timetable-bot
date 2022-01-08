import requests

from app.core.config import settings
from asc_scrapper.crud import get_schedule_by_class_name, get_periods, get_days
from asc_scrapper.schedule_html import schedule_html
from asc_scrapper.schemas import Schedule


def get_schedule_image(name: str, test: bool = True):
    schedule: Schedule = get_schedule_by_class_name(name)
    url = settings().HTML_TO_IMAGE_SERVICE + "image"

    data = schedule_html(periods=get_periods(), days=get_days(), cards=schedule, title=name, is_dark=True)

    response = requests.get(url, data={"html": data}, stream=True)
    url = response.json()["url"]
    img_data = requests.get(url).content
    with open(f'generated_data/{name}table.png', 'wb') as handler:
        handler.write(img_data)
    if test:
        with open("generated_data/table.g.html", "w", encoding="utf-8") as file:
            file.write(data)

    return url


if __name__ == '__main__':
    get_schedule_image("ثالث برمجيات صباحي", test=True)

# matlab -38
# classroom_schedule("-38")
# class_schedule("*22")
# ولاء *58
# teacher_schedule("*24")
# print("\n".join([f"{teacher.short}, {teacher.id}" for teacher in get_teachers()]))
