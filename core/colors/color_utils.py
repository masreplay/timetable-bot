from random import randint
from typing import List, Any

from core.colors.primaries import *
from core.colors.accent import *

primaries: List[MaterialColor] = [
    red,
    pink,
    purple,
    deepPurple,
    indigo,
    blue,
    lightBlue,
    cyan,
    teal,
    green,
    lightGreen,
    lime,
    yellow,
    amber,
    orange,
    deepOrange,
    brown,
]

accents: List[MaterialAccentColor] = [
    red_accent,
    pink_accent,
    purple_accent,
    deep_purple_accent,
    indigo_accent,
    blue_accent,
    light_blue_accent,
    cyan_accent,
    teal_accent,
    green_accent,
    light_green_accent,
    lime_accent,
    yellow_accent,
    amber_accent,
    orange_accent,
    deep_orange_accent,
]


def decide_text_color(bg_color: Color) -> str:
    n_threshold = 105
    color = bg_color.as_rgb_tuple()
    bg_delta = (color[0] * 0.299) + (color[1] * 0.587) + (color[2] * 0.114)

    return "#000000" if ((255 - bg_delta) < n_threshold) else "#ffffff"


def reduce_color_lightness(in_color: Color, in_amount: float) -> Color:
    """
    reduce the lightness of color
    """
    color = in_color.as_rgb_tuple()
    return Color((
        min(255, int(color[0] * in_amount)),
        min(255, int(color[1] * in_amount)),
        min(255, int(color[2] * in_amount))
    ))


def random_primary(shade: int = 300) -> Color:
    assert shade in [50, 100, 200, 300, 400, 500, 600, 700, 800, 900], "Choose shade from range"
    return primaries[randint(0, len(primaries) - 1)].shades[shade]


def random_accent(shade: int = 200) -> Color:
    assert shade in [100, 200, 400, 700], "Choose shade from range"
    return accents[randint(0, len(accents) - 1)].shades[shade]


def get_color_escape(color: Color, background=False) -> str:
    color = color.as_rgb_tuple()
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, color[0], color[1], color[2])


def colored_text(value: Any, bg_color: Color) -> str:
    """ Color console color to be printed  """
    reset = '\033[0m'

    return f"{get_color_escape(Color(decide_text_color(bg_color)))}{get_color_escape(bg_color, True)}{value}" \
           f"{reset}"


def cprint(value: Any, bg_color: Color) -> Any:
    print(colored_text(value, bg_color=bg_color))


if __name__ == '__main__':
    bg = Color('64b5f6')
    text_color = decide_text_color(Color('64b5f6'))
    print(reduce_color_lightness(Color('64b5f6'), 0.1))
    cprint("test", bg_color=bg)
