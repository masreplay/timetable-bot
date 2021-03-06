import pathlib

import requests
from pydantic.color import Color

from app import schemas
from app.core.config import settings
from app.schemas.enums import Environment
from app.schemas.image_url import ImageUrl
from ui.color import Theme
from ui.colors.color_utils import decide_text_color, cprint


def schedule_html_template(
        *,
        schedule: schemas.ScheduleDetails,
        theme: Theme
):
    """
    Template body of schedule
    """
    col_width = 100 / (len(schedule.periods) + 1)
    row_height = 100 / (len(schedule.days) + 1)
    style = f"""<style>
        table {{
            border: 1px solid {theme.colors.outline};
            border-collapse: separate;
            border-left: 0;
            border-radius: 10px;
            border-spacing: 0px;
            width: 100%;
            height: 100%;
        }}

        body, div, h1, h2, h3, h4, h5, h6, p, span {{
            font-family: {theme.font_name}!important;
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
            color: {theme.colors.background};
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
            border-left: 1px solid {theme.colors.outline};
        }}

        td {{
            border-top: 1px solid {theme.colors.outline};
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
            families: ['{theme.font_name}']
            }}
          }});
        </script>
</head>

<body>
    <div style="background-color: {theme.colors.background}; padding: 1%;">
        <h1 style="color: {theme.colors.on_background}; text-align: center;">{schedule.item.name}</h1>
        <table>
            <thead>
                <colgroup>
                    <col span="{len(schedule.periods) + 1}" width="{col_width}%">
                </colgroup>
                <tr>
                    <th></th>
                    {"".join([f'<th style="color: {theme.colors.on_background}">{period.time}</th>' for period in schedule.periods])} 
                </tr>
            </thead>
            <tbody>{generate_table(schedule=schedule, theme=theme)}</tbody>
        </table>
    </div>
</body>

</html>"""


# </table>
#         <!-- <div style="display: flex; justify-content: space-between; flex-direction: row-reverse">
#             <h3 style="color: {theme.colors.on_background}">{schedule.information.get_validate_date}</h3>
#             <h3 style="color: {theme.colors.on_background}">Telegram: {schedule.information.bot_telegram_id}</h3>
#         </div> -->

def generate_table(*, schedule: schemas.ScheduleDetails, theme: Theme):
    """
    HTML Table body period cross days
    """
    card_tags = ""

    for day in schedule.days:
        row = []
        for period in schedule.periods:
            card: schemas.CardScheduleDetails = next(
                filter(
                    lambda card: card.period_id == period.id and card.day_id == day.id,
                    schedule.cards,
                ),
                None,
            )

            if card:
                teacher: schemas.TeacherSchedule | None = card.lesson.teacher

                color: Color = Color(teacher.color) if teacher else Color("#ffffff")

                font_color = decide_text_color(color)
                row.append(
                    f"<td "
                    f'style="background-color: {color}; color: {font_color}">'
                    f"{card_table(card=card, color=color)}</td>"
                )
            else:
                row.append(f"<td></td>")

        card_tags += f'<tr><td style="color: {theme.colors.on_background}"><h2>{day.name}</h2></td>{"".join(row)}</tr>'
        row.clear()

    return card_tags


def card_table(*, card: schemas.CardScheduleDetails, color: Color):
    """
    HTML Table's card
    """
    subject_name = card.lesson.subject.name
    tags = [f"<h3>{subject_name}</h3>"]
    if card.lesson.room:
        tags.append(f"<p><b>{card.lesson.room.name}</b></p>")

    if card.lesson.teacher:
        tags.append(f"<p>{card.lesson.teacher.name}</p>")

    cprint(
        f"{subject_name} - {card.lesson.teacher.name if card.lesson.teacher else ''} "
        f"- {card.lesson.room.name if card.lesson.room else ''}",
        bg_color=color,
    )
    return "".join(tags)


def get_schedule_image(
        *, schedule: schemas.ScheduleDetails, theme: Theme
) -> str | None:
    """
    Generate schedule image from stage id

    :return: str schedule image url or null
    """

    html = schedule_html_template(
        schedule=schedule, theme=theme
    )

    response = requests.post(
        f"{settings().HTML_TO_IMAGE_SERVICE}/image",
        data={"html": html},
        stream=True,
    )

    image_url = ImageUrl.parse_obj(response.json())
    img_data = requests.get(image_url.url).content

    if settings().ENVIRONMENT == Environment.development:
        print(image_url.url)
        pathlib.Path("generated_data").mkdir(parents=True, exist_ok=True)
        with open(f"generated_data/{schedule.item.name}table.png", "wb") as handler:
            handler.write(img_data)
            with open("generated_data/table.g.html", "w", encoding="utf-8") as file:
                file.write(html)

    return image_url.url


if __name__ == "__main__":
    pass
