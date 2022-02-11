from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from fastapi import Depends
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from app import crud
from app.db.db import get_db
from bot_app.schedule_html import schedule_html_template
from bot_app.theme import DARK_THEME, LIGHT_THEME

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def read_stage_ui(
        stage_id: UUID,
        is_dark: Optional[bool] = Query(False),
        db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve Stage uri.
    """

    stage = crud.stage.get(db=db, id=stage_id)
    if not stage:
        raise HTTPException(status_code=204, detail="Stage not found")
    schedule = crud.schedule.get(db=db, stage_id=stage_id)

    return HTMLResponse(
        content=schedule_html_template(
            schedule=schedule,
            title=stage.name,
            theme=DARK_THEME if is_dark else LIGHT_THEME,
            creators_name="@ConstructorTeam"
        )
    )
