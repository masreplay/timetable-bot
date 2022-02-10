from typing import Any

from fastapi import APIRouter

from bot_app.theme import THEMES, NamedTheme

router = APIRouter()


@router.get("/", response_model=list[NamedTheme])
def read_theme() -> Any:
    """
    Retrieve themes.
    """
    return THEMES
