import pathlib
from random import Random
from uuid import UUID

import requests
from pydantic.color import Color

from app import schemas
from app.core.config import settings
from app.schemas.enums import Environment
from asc_scrapper.test import ImageUrl
from bot_app import service
from bot_app.template import schedule_template_html
from bot_app.theme import ScheduleTheme, DARK_THEME, LIGHT_THEME
from colors.color_utils import decide_text_color, cprint, primaries


def generate_table(*, schedule: schemas.ScheduleDetails, theme: ScheduleTheme):
    """
    HTML Table body period cross days
    """
    card_tags = ""

    for day in schedule.days:
        row = []
        for period in schedule.periods:
            card: schemas.CardScheduleDetails = next(
                filter(lambda card: card.period_id == period.id and card.day_id == day.id,
                       schedule.cards), None)

            if card:
                teacher: schemas.TeacherSchedule | None = card.lesson.teacher
                # color = Color(teacher.color if teacher else "#ffffff")
                # color = reduce_color_lightness(color, 0.75)
                color = Color(Random().choice(primaries).shades[200].as_hex())
                font_color = decide_text_color(color)
                row.append(
                    f'<td '
                    f'style="background-color: {color}; color: {font_color}">'
                    f'{card_table(card=card, color=color)}</td>'
                )
            else:
                row.append(f"<td></td>")

        card_tags += f'<tr><td style="color: {theme.on_background_color}"><h2>{day.name}</h2></td>{"".join(row)}</tr>'
        row.clear()

    return card_tags


def card_table(*, card: schemas.CardScheduleDetails, color: Color):
    """
    HTML Table's card
    """
    subject_name = card.lesson.subject.name
    tags = [f"<p>{subject_name}</p>"]
    if card.lesson.room:
        tags.append(f"<p><b>{card.lesson.room.name}</b></p>")

    if card.lesson.teacher:
        tags.append(f'<p>{card.lesson.teacher.name}</p>')

    cprint(
        f"{subject_name} - {card.lesson.teacher.name if card.lesson.teacher else ''} "
        f"- {card.lesson.room.name if card.lesson.room else ''}",
        bg_color=color)
    return "".join(tags)


def get_stage_schedule_image(*, stage_id: UUID, name: str, is_dark: bool = False) -> str | None:
    """
    Generate schedule image from stage id
    """

    theme = DARK_THEME if is_dark else LIGHT_THEME
    response = service.get_stage_schedule(stage_id)
    if response.status_code == 200:
        schedule = schemas.ScheduleDetails.parse_obj(response.json())

        data = schedule_template_html(schedule=schedule, title=name, theme=theme)

        response = requests.post(f"{settings().HTML_TO_IMAGE_SERVICE}/image", data={"html": data}, stream=True)
        image_url = ImageUrl.parse_obj(response.json())
        img_data = requests.get(image_url.url).content

        if settings().ENVIRONMENT == Environment.development:
            print(image_url.url)
            pathlib.Path("generated_data").mkdir(parents=True, exist_ok=True)
            with open(f'generated_data/{name}table.png', 'wb') as handler:
                handler.write(img_data)
                with open("generated_data/table.g.html", "w", encoding="utf-8") as file:
                    file.write(data)

        return image_url.url


if __name__ == '__main__':
    get_stage_schedule_image(stage_id=UUID("0ca31629-cea3-4568-8bd4-c9fb77f77114"), name="ثالث برمجيات صباحي")
