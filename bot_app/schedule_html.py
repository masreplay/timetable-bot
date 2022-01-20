import pathlib

import requests
from pydantic.color import Color

from app import schemas
from app.core.config import settings
from asc_scrapper.test import ImageUrl
from colors.color_utils import decide_text_color, reduce_color_lightness, cprint

IMAGE_URL = f"{settings().HTML_TO_IMAGE_SERVICE}/image"


def schedule_html(*, schedule: schemas.ScheduleDetails, title: str, is_dark: bool):
    col_width = 100 / (len(schedule.periods) + 1)
    row_height = 100 / (len(schedule.days) + 1)
    style = f"""<style>
        table {{
            border: 1px solid #ddd;
            border-collapse: separate;
            border-left: 0;
            border-radius: 10px;
            border-spacing: 0px;
            width: 100%;
            height: 100%;
        }}
        
        body, div, h1, h2, h3, h4, h5, h6, p, span {{
            font-family: Tajawal!important;
            -webkit-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }}

        h2 {{
           display:inline;
           margin-top:40px;
           text-align:center;
        }}
        thead {{
            display: table-header-group;
            vertical-align: middle;
            border-color: inherit;
            border-collapse: separate;
        }}

        th {{
            color: black;
        }}

        tr {{
            display: table-row;
            vertical-align: inherit;
            border-color: inherit;
        }}

        th,
        td {{
            padding: 4px;
            white-space:pre-wrap;
            height: {row_height}%;
            word-wrap:break-word;
            text-align: middle;
            vertical-align: middle;
            border-left: 1px solid #ddd;
        }}

        td {{
            border-top: 1px solid #ddd;
            text-align: center;
        }}

        thead:first-child tr:first-child th:first-child,
        tbody:first-child tr:first-child td:first-child {{
            border-radius: 4px 0 0 0;
        }}

        thead:last-child tr:last-child th:first-child,
        tbody:last-child tr:last-child td:first-child {{
            border-radius: 0 0 0 4px;
        }}
    </style>"""
    return f"""<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    {style}
    <script src="https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js"></script>
        <script>
          WebFont.load({{
            google: {{
            families: ['Tajawal']
            }}
          }});
        </script>
</head>

<body>
    <div style="background-color: {"#202b36" if is_dark else "white"}; padding: 1%;">
        <h1 style="color: white; text-align: center;">{title}</h1>
        <table>
            <thead>
                <colgroup>
                    <col span="{len(schedule.periods) + 1}" width="{col_width}%">
                </colgroup>
                <tr>
                    <th></th>
                    {"".join([f'<th style="color: #ffffff">{period.time}</th>' for period in schedule.periods])}
                </tr>
            </thead>
            <tbody>{generate_table(schedule=schedule)}</tbody>
        </table>
        <h3 style="color: white; text-align: right;">@ConstructorTeam</h1>
    </div>
</body>

</html>"""


def generate_table(schedule: schemas.ScheduleDetails, is_dark: bool = True):
    card_tags = ""
    on_background_color = "#ffffff" if is_dark else "#000000"

    for day in schedule.days:
        row = []
        for period in schedule.periods:
            card: schemas.CardScheduleDetails = next(
                filter(lambda card: card.period_id == period.id and card.day_id == day.id,
                       schedule.cards), None)

            if card:
                teacher: schemas.TeacherSchedule | None = card.lesson.teacher
                color: Color = Color(teacher.color if teacher else "#ffffff")
                color = reduce_color_lightness(color, 0.75)
                font_color = decide_text_color(color)
                row.append(
                    f'<td '
                    f'style="background-color: {color}; color: {font_color}">'
                    f'{card_into_table(card=card, color=color)}</td>'
                )
            else:
                row.append(f"<td></td>")

        card_tags += f'<tr><td style="color: {on_background_color}"><h2>{day.name}</h2></td>{"".join(row)}</tr>'
        row.clear()

    return card_tags


def card_into_table(*, card: schemas.CardScheduleDetails, color: Color):
    subject_name = card.lesson.subject.name
    # classroom = lesson.c
    tags = [f"<p>{subject_name}</p>"]
    if card.lesson.room:
        tags.append(f"<p><b>{card.lesson.room.name}</b></p>")

    if card.lesson.teacher:
        tags.append(f'<p style="font-family: Tajawal;">{card.lesson.teacher.name}</p>')

    cprint(f"{subject_name} - {card.lesson.teacher.name if card.lesson.teacher else ''} - {card.lesson.room.name}",
           bg_color=color)
    return "".join(tags)


def get_schedule_image(*, stage_id: str, name: str, test: bool = True) -> str | None:
    response = requests.get(url=f"{settings().FAST_API_HOST}/schedule/stage/{stage_id}")
    if response.status_code == 200:
        schedule = schemas.ScheduleDetails.parse_obj(response.json())

        data = schedule_html(schedule=schedule, title=name, is_dark=True)

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
    get_schedule_image("9f1703de-cce5-41f5-b9b4-1f2d041578f0", "ثالث برمجيات صباحي", test=True)
