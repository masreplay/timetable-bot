from random import randint
from typing import List

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


def decide_text_color(bg_color: Color):
    n_threshold = 105
    color = bg_color.as_rgb_tuple()
    bg_delta = (color[0] * 0.299) + (color[1] * 0.587) + (color[2] * 0.114)

    return "#000000" if ((255 - bg_delta) < n_threshold) else "#ffffff"


def random_primary():
    return primaries[randint(0, len(primaries) - 1)].shades[300]


print(decide_text_color(Color('64b5f6')))
