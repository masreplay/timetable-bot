from enum import Enum

from pydantic import BaseModel
from pydantic.color import Color

from ui.directionality import Directionality
from ui.language import Language


class ColorTheme(BaseModel):
    """
    m3 material design you plate
    """
    primary: Color
    on_primary: Color
    primary_container: Color
    on_primary_container: Color
    secondary: Color
    on_secondary: Color
    secondary_container: Color
    on_secondary_container: Color
    tertiary: Color
    on_tertiary: Color
    tertiary_container: Color
    on_tertiary_container: Color
    error: Color
    error_container: Color
    on_error: Color
    on_error_container: Color
    background: Color
    on_background: Color
    surface: Color
    on_surface: Color
    surface_variant: Color
    on_surface_variant: Color
    outline: Color
    inverse_on_surface: Color
    inverse_surface: Color
    inverse_primary: Color
    shadow: Color


dark_theme = ColorTheme(
    primary=Color("#abc7ff"),
    on_primary=Color("#002e6a"),
    primary_container=Color("#034490"),
    on_primary_container=Color("#d6e2ff"),
    secondary=Color("#bec6dc"),
    on_secondary=Color("#283041"),
    secondary_container=Color("#3f4759"),
    on_secondary_container=Color("#dae2f9"),
    tertiary=Color("#debce0"),
    on_tertiary=Color("#3f2843"),
    tertiary_container=Color("#573e5b"),
    on_tertiary_container=Color("#fbd8fc"),
    error=Color("#ffb4a9"),
    error_container=Color("#930006"),
    on_error=Color("#680003"),
    on_error_container=Color("#ffdad4"),
    background=Color("#1b1b1d"),
    on_background=Color("#e4e2e6"),
    surface=Color("#1b1b1d"),
    on_surface=Color("#e4e2e6"),
    surface_variant=Color("#44474f"),
    on_surface_variant=Color("#c4c6d0"),
    outline=Color("#8e9099"),
    inverse_on_surface=Color("#1b1b1d"),
    inverse_surface=Color("#e4e2e6"),
    inverse_primary=Color("#2c5daa"),
    shadow=Color("#000000"),
)

light_theme = ColorTheme(
    primary=Color("#2c5daa"),
    on_primary=Color("#ffffff"),
    primary_container=Color("#d6e2ff"),
    on_primary_container=Color("#001a42"),
    secondary=Color("#565e71"),
    on_secondary=Color("#ffffff"),
    secondary_container=Color("#dae2f9"),
    on_secondary_container=Color("#131c2c"),
    tertiary=Color("#705573"),
    on_tertiary=Color("#ffffff"),
    tertiary_container=Color("#fbd8fc"),
    on_tertiary_container=Color("#29132e"),
    error=Color("#ba1b1b"),
    error_container=Color("#ffdad4"),
    on_error=Color("#ffffff"),
    on_error_container=Color("#410001"),
    background=Color("#fdfbff"),
    on_background=Color("#1b1b1d"),
    surface=Color("#fdfbff"),
    on_surface=Color("#1b1b1d"),
    surface_variant=Color("#e1e2ec"),
    on_surface_variant=Color("#44474f"),
    outline=Color("#74777f"),
    inverse_on_surface=Color("#f2f0f4"),
    inverse_surface=Color("#2f3033"),
    inverse_primary=Color("#abc7ff"),
    shadow=Color("#000000"),
)


class ColorThemeType(str, Enum):
    dark = "dark"
    light = "light"


colors_theme: dict[ColorThemeType, ColorTheme] = {
    ColorThemeType.dark: dark_theme,
    ColorThemeType.light: light_theme,
}


class Theme(BaseModel):
    colors: ColorTheme
    language: Language
    directionality: Directionality = Directionality.ltr
    font_name: str = "Tajawal"
