from dataclasses import dataclass

from pydantic import BaseModel
from pydantic.color import Color

from colors.color_utils import reduce_color_lightness, random_primary


class ScheduleTheme(BaseModel):
    background_color: str
    on_background_color: str

    primary_color: str
    on_primary_color: str

    divider_color: str
    font_name: str = "Tajawal"


class NamedTheme(BaseModel):
    name: str
    theme: ScheduleTheme


def random_light() -> str:
    return random_primary(200).as_hex()


def random_dark(shade: int = 200, reduce: float = 0.95) -> str:
    assert (reduce <= 1)
    color = random_primary(shade)
    return reduce_color_lightness(color, reduce).as_hex()


# material shade 200 , reduce 0.95 or shade only 400
DARK_THEME = ScheduleTheme(background_color="#1f1f1f", on_background_color="#ffffff",
                           primary_color="#FFF700", on_primary_color="#000000",
                           divider_color="#dddddd")

# material shade 200
LIGHT_THEME = ScheduleTheme(background_color="#ffffff", on_background_color="#000000",
                            primary_color="#FFF700", on_primary_color="#000000",
                            divider_color="#dddddd")

THEMES = [
    NamedTheme(name="Dark", theme=DARK_THEME),
    NamedTheme(name="Light", theme=LIGHT_THEME),
]
