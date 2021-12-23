import shutil

import requests

from asc_scrapper.schedule_html import schedule_html
from asc_scrapper.view import *
from config import get_settings

# matlab -38
# classroom_schedule("-38")
# class_schedule("*22")
# ولاء *58
# teacher_schedule("*24")
# print("\n".join([f"{teacher.short}, {teacher.id}" for teacher in get_teachers()]))


def main():
    schedule: Schedule = teacher_schedule("*15")
    url = get_settings().html_to_image_service

    data = schedule_html(periods=get_periods(), days=get_days(), cards=schedule)

    response = requests.get(url, data={"html": data}, stream=True)

    with open("table.g.html", "w", encoding="utf-8") as file:
        file.write(data)

    with open('table.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


if __name__ == '__main__':
    main()
