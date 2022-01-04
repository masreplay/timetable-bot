from pydantic.color import Color

from colors.primaries import MaterialAccentColor


_pink_accent_primary_value = 'FF4081'
_purple_accent_primary_value = 'E040FB'
_deep_purple_accent_primary_value = '7C4DFF'
_indigo_accent_primary_value = '536DFE'
_blue_accent_primary_value = '448AFF'
_light_blue_accent_primary_value = '40C4FF'
_cyan_accent_primary_value = '18FFFF'
_teal_accent_primary_value = '64FFDA'
_green_accent_primary_value = '69F0AE'
_light_green_accent_primary_value = 'B2FF59'
_lime_accent_primary_value = 'EEFF41'
_yellow_accent_primary_value = 'FFFF00'
_amber_accent_primary_value = 'FFD740'
_orange_accent_primary_value = 'FFAB40'
_deep_orange_accent_primary_value = 'FF6E40'
_red_accent_value = 'FF5252'

red_accent = MaterialAccentColor(
    primary_color=_red_accent_value,
    shades={
        100: Color('FF8A80'),
        200: Color(_red_accent_value),
        400: Color('FF1744'),
        700: Color('D50000'),
    },
);

pink_accent = MaterialAccentColor(
    primary_color=_pink_accent_primary_value,
    shades={
        100: Color('FF80AB'),
        200: Color(_pink_accent_primary_value),
        400: Color('F50057'),
        700: Color('C51162'),
    },
)

purple_accent = MaterialAccentColor(
    primary_color=_purple_accent_primary_value,
    shades={
        100: Color('EA80FC'),
        200: Color(_purple_accent_primary_value),
        400: Color('D500F9'),
        700: Color('AA00FF'),
    },
)

deep_purple_accent = MaterialAccentColor(
    primary_color=_deep_purple_accent_primary_value,
    shades={
        100: Color('B388FF'),
        200: Color(_deep_purple_accent_primary_value),
        400: Color('651FFF'),
        700: Color('6200EA'),
    },
)

indigo_accent = MaterialAccentColor(
    primary_color=_indigo_accent_primary_value,
    shades={
        100: Color('8C9EFF'),
        200: Color(_indigo_accent_primary_value),
        400: Color('3D5AFE'),
        700: Color('304FFE'),
    },
)

blue_accent = MaterialAccentColor(
    primary_color=_blue_accent_primary_value,
    shades={
        100: Color('82B1FF'),
        200: Color(_blue_accent_primary_value),
        400: Color('2979FF'),
        700: Color('2962FF'),
    },
)

light_blue_accent = MaterialAccentColor(
    primary_color=_light_blue_accent_primary_value,
    shades={
        100: Color('80D8FF'),
        200: Color(_light_blue_accent_primary_value),
        400: Color('00B0FF'),
        700: Color('0091EA'),
    },
)

cyan_accent = MaterialAccentColor(
    primary_color=_cyan_accent_primary_value,
    shades={
        100: Color('84FFFF'),
        200: Color(_cyan_accent_primary_value),
        400: Color('00E5FF'),
        700: Color('00B8D4'),
    },
)

teal_accent = MaterialAccentColor(
    primary_color=_teal_accent_primary_value,
    shades={
        100: Color('A7FFEB'),
        200: Color(_teal_accent_primary_value),
        400: Color('1DE9B6'),
        700: Color('00BFA5'),
    },
)

green_accent = MaterialAccentColor(
    primary_color=_green_accent_primary_value,
    shades={
        100: Color('B9F6CA'),
        200: Color(_green_accent_primary_value),
        400: Color('00E676'),
        700: Color('00C853'),
    },
)

light_green_accent = MaterialAccentColor(
    primary_color=_light_green_accent_primary_value,
    shades={
        100: Color('CCFF90'),
        200: Color(_light_green_accent_primary_value),
        400: Color('76FF03'),
        700: Color('64DD17'),
    },
)

lime_accent = MaterialAccentColor(
    primary_color=_lime_accent_primary_value,
    shades={
        100: Color('F4FF81'),
        200: Color(_lime_accent_primary_value),
        400: Color('C6FF00'),
        700: Color('AEEA00'),
    },
)

yellow_accent = MaterialAccentColor(
    primary_color=_yellow_accent_primary_value,
    shades={
        100: Color('FFFF8D'),
        200: Color(_yellow_accent_primary_value),
        400: Color('FFEA00'),
        700: Color('FFD600'),
    },
)

amber_accent = MaterialAccentColor(
    primary_color=_amber_accent_primary_value,
    shades={
        100: Color('FFE57F'),
        200: Color(_amber_accent_primary_value),
        400: Color('FFC400'),
        700: Color('FFAB00'),
    },
)

orange_accent = MaterialAccentColor(
    primary_color=_orange_accent_primary_value,
    shades={
        100: Color('FFD180'),
        200: Color(_orange_accent_primary_value),
        400: Color('FF9100'),
        700: Color('FF6D00'),
    },
)

deep_orange_accent = MaterialAccentColor(
    primary_color=_deep_orange_accent_primary_value,
    shades={
        100: Color('FF9E80'),
        200: Color(_deep_orange_accent_primary_value),
        400: Color('FF3D00'),
        700: Color('DD2C00'),
    },
)
