from pydantic import BaseModel
from pydantic.color import Color


class MaterialColor(BaseModel):
    primary_color: str
    shades: dict[int, Color]


class MaterialAccentColor(MaterialColor):
    pass


_red_primary_value = 'F44336'
_pink_primary_value = 'E91E63'
_purple_primary_value = '9C27B0'
_deep_purple_primary_value = '673AB7'
_indigo_primary_value = '3F51B5'
_blue_primary_value = '2196F3'
_light_blue_primary_value = '03A9F4'
_cyan_primary_value = '00BCD4'
_teal_primary_value = '009688'
_green_primary_value = '4CAF50'
_light_green_primary_value = '8BC34A'
_lime_primary_value = 'CDDC39'
_yellow_primary_value = 'FFEB3B'
_amber_primary_value = 'FFC107'
_orange_primary_value = 'FF9800'
_deep_orange_primary_value = 'FF5722'
_brown_primary_value = '795548'
_blue_grey_primary_value = '607D8B'
_grey_primary_value = 'BDBDBD'

red = MaterialColor(
    primary_color=_red_primary_value,
    shades={
        50: Color('FFEBEE'),
        100: Color('FFCDD2'),
        200: Color('EF9A9A'),
        300: Color('E57373'),
        400: Color('EF5350'),
        500: Color(_red_primary_value),
        600: Color('E53935'),
        700: Color('D32F2F'),
        800: Color('C62828'),
        900: Color('B71C1C'),
    },
)

pink = MaterialColor(
    primary_color=_pink_primary_value,
    shades={
        50: Color('FCE4EC'),
        100: Color('F8BBD0'),
        200: Color('F48FB1'),
        300: Color('F06292'),
        400: Color('EC407A'),
        500: Color(_pink_primary_value),
        600: Color('D81B60'),
        700: Color('C2185B'),
        800: Color('AD1457'),
        900: Color('880E4F'),
    },
)

purple = MaterialColor(
    primary_color=_purple_primary_value,
    shades={
        50: Color('F3E5F5'),
        100: Color('E1BEE7'),
        200: Color('CE93D8'),
        300: Color('BA68C8'),
        400: Color('AB47BC'),
        500: Color(_purple_primary_value),
        600: Color('8E24AA'),
        700: Color('7B1FA2'),
        800: Color('6A1B9A'),
        900: Color('4A148C'),
    },
)

deepPurple = MaterialColor(
    primary_color=_deep_purple_primary_value,
    shades={
        50: Color('EDE7F6'),
        100: Color('D1C4E9'),
        200: Color('B39DDB'),
        300: Color('9575CD'),
        400: Color('7E57C2'),
        500: Color(_deep_purple_primary_value),
        600: Color('5E35B1'),
        700: Color('512DA8'),
        800: Color('4527A0'),
        900: Color('311B92'),
    },
)

indigo = MaterialColor(
    primary_color=_indigo_primary_value,
    shades={
        50: Color('E8EAF6'),
        100: Color('C5CAE9'),
        200: Color('9FA8DA'),
        300: Color('7986CB'),
        400: Color('5C6BC0'),
        500: Color(_indigo_primary_value),
        600: Color('3949AB'),
        700: Color('303F9F'),
        800: Color('283593'),
        900: Color('1A237E'),
    },
)

blue = MaterialColor(
    primary_color=_blue_primary_value,
    shades={
        50: Color('E3F2FD'),
        100: Color('BBDEFB'),
        200: Color('90CAF9'),
        300: Color('64B5F6'),
        400: Color('42A5F5'),
        500: Color(_blue_primary_value),
        600: Color('1E88E5'),
        700: Color('1976D2'),
        800: Color('1565C0'),
        900: Color('0D47A1'),
    },
)

lightBlue = MaterialColor(
    primary_color=_light_blue_primary_value,
    shades={
        50: Color('E1F5FE'),
        100: Color('B3E5FC'),
        200: Color('81D4FA'),
        300: Color('4FC3F7'),
        400: Color('29B6F6'),
        500: Color(_light_blue_primary_value),
        600: Color('039BE5'),
        700: Color('0288D1'),
        800: Color('0277BD'),
        900: Color('01579B'),
    },
)

cyan = MaterialColor(
    primary_color=_cyan_primary_value,
    shades={
        50: Color('E0F7FA'),
        100: Color('B2EBF2'),
        200: Color('80DEEA'),
        300: Color('4DD0E1'),
        400: Color('26C6DA'),
        500: Color(_cyan_primary_value),
        600: Color('00ACC1'),
        700: Color('0097A7'),
        800: Color('00838F'),
        900: Color('006064'),
    },
)

teal = MaterialColor(
    primary_color=_teal_primary_value,
    shades={
        50: Color('E0F2F1'),
        100: Color('B2DFDB'),
        200: Color('80CBC4'),
        300: Color('4DB6AC'),
        400: Color('26A69A'),
        500: Color(_teal_primary_value),
        600: Color('00897B'),
        700: Color('00796B'),
        800: Color('00695C'),
        900: Color('004D40'),
    },
)

green = MaterialColor(
    primary_color=_green_primary_value,
    shades={
        50: Color('E8F5E9'),
        100: Color('C8E6C9'),
        200: Color('A5D6A7'),
        300: Color('81C784'),
        400: Color('66BB6A'),
        500: Color(_green_primary_value),
        600: Color('43A047'),
        700: Color('388E3C'),
        800: Color('2E7D32'),
        900: Color('1B5E20'),
    },
)

lightGreen = MaterialColor(
    primary_color=_light_green_primary_value,
    shades={
        50: Color('F1F8E9'),
        100: Color('DCEDC8'),
        200: Color('C5E1A5'),
        300: Color('AED581'),
        400: Color('9CCC65'),
        500: Color(_light_green_primary_value),
        600: Color('7CB342'),
        700: Color('689F38'),
        800: Color('558B2F'),
        900: Color('33691E'),
    },
)

lime = MaterialColor(
    primary_color=_lime_primary_value,
    shades={
        50: Color('F9FBE7'),
        100: Color('F0F4C3'),
        200: Color('E6EE9C'),
        300: Color('DCE775'),
        400: Color('D4E157'),
        500: Color(_lime_primary_value),
        600: Color('C0CA33'),
        700: Color('AFB42B'),
        800: Color('9E9D24'),
        900: Color('827717'),
    },
)

yellow = MaterialColor(
    primary_color=_yellow_primary_value,
    shades={
        50: Color('FFFDE7'),
        100: Color('FFF9C4'),
        200: Color('FFF59D'),
        300: Color('FFF176'),
        400: Color('FFEE58'),
        500: Color(_yellow_primary_value),
        600: Color('FDD835'),
        700: Color('FBC02D'),
        800: Color('F9A825'),
        900: Color('F57F17'),
    },
)

amber = MaterialColor(
    primary_color=_amber_primary_value,
    shades={
        50: Color('FFF8E1'),
        100: Color('FFECB3'),
        200: Color('FFE082'),
        300: Color('FFD54F'),
        400: Color('FFCA28'),
        500: Color(_amber_primary_value),
        600: Color('FFB300'),
        700: Color('FFA000'),
        800: Color('FF8F00'),
        900: Color('FF6F00'),
    },
)

orange = MaterialColor(
    primary_color=_orange_primary_value,
    shades={
        50: Color('FFF3E0'),
        100: Color('FFE0B2'),
        200: Color('FFCC80'),
        300: Color('FFB74D'),
        400: Color('FFA726'),
        500: Color(_orange_primary_value),
        600: Color('FB8C00'),
        700: Color('F57C00'),
        800: Color('EF6C00'),
        900: Color('E65100'),
    },
)

deepOrange = MaterialColor(
    primary_color=_deep_orange_primary_value,
    shades={
        50: Color('FBE9E7'),
        100: Color('FFCCBC'),
        200: Color('FFAB91'),
        300: Color('FF8A65'),
        400: Color('FF7043'),
        500: Color(_deep_orange_primary_value),
        600: Color('F4511E'),
        700: Color('E64A19'),
        800: Color('D84315'),
        900: Color('BF360C'),
    },
)

brown = MaterialColor(
    primary_color=_brown_primary_value,
    shades={
        50: Color('EFEBE9'),
        100: Color('D7CCC8'),
        200: Color('BCAAA4'),
        300: Color('A1887F'),
        400: Color('8D6E63'),
        500: Color(_brown_primary_value),
        600: Color('6D4C41'),
        700: Color('5D4037'),
        800: Color('4E342E'),
        900: Color('3E2723'),
    },
)

grey = MaterialColor(
    primary_color=_grey_primary_value,
    shades={
        50: Color('FAFAFA'),
        100: Color('F5F5F5'),
        200: Color('EEEEEE'),
        300: Color('E0E0E0'),
        350: Color('D6D6D6'),
        400: Color('BDBDBD'),
        500: Color(_grey_primary_value),
        600: Color('757575'),
        700: Color('616161'),
        800: Color('424242'),
        850: Color('303030'),
        900: Color('212121'),
    },
)

blueGrey = MaterialColor(
    primary_color=_blue_grey_primary_value,
    shades={
        50: Color('ECEFF1'),
        100: Color('CFD8DC'),
        200: Color('B0BEC5'),
        300: Color('90A4AE'),
        400: Color('78909C'),
        500: Color(_blue_grey_primary_value),
        600: Color('546E7A'),
        700: Color('455A64'),
        800: Color('37474F'),
        900: Color('263238'),
    },
)
