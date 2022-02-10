from typing import Any

from fastapi import APIRouter

from bot_app.theme import ScheduleTheme, DARK_THEME, LIGHT_THEME

router = APIRouter()


@router.get("/", response_model=dict)
def read_theme() -> Any:
    """
    Retrieve theme.
    """
    return {
        "light_theme": LIGHT_THEME,
        "dark_theme": DARK_THEME,
    }
