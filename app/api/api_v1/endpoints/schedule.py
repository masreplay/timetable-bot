from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.schedule import ScheduleDetails
from app.schemas.schemas import ImageUrl
from ui.color import Theme, ColorThemeType, colors_theme
from ui.directionality import Directionality
from ui.language import Language
from ui.view.schedule_html import get_stage_schedule_image

router = APIRouter()


@router.get("/all", response_model=schemas.ScheduleSchemas)
def read_all_schedule(
        db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve all schedules data.
    """
    return crud.schedule.get_multi(db=db)


@router.get("/", response_model=ScheduleDetails)
def read_schedule(
        stage_id: UUID | None = Query(None),
        teacher_id: UUID | None = None,
        room_id: UUID | None = None,
        lesson_id: UUID | None = None,
        db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve Single schedule.
    q2
    """

    if not stage_id and not teacher_id and not room_id and not lesson_id:
        return crud.schedule.default(db=db)

    stage = crud.stage.get(db=db, id=stage_id)
    return crud.schedule.get(db=db, stage_id=stage_id, teacher_id=teacher_id, room_id=room_id, stage=stage)


@router.get("/image", response_model=ImageUrl)
def get_schedule_image_url(
        stage_id: UUID,
        theme: ColorThemeType | None = ColorThemeType.light,
        language: Language | None = Language.ar,
        directionality: Directionality | None = Directionality.ltr,
        db: Session = Depends(get_db),
) -> Any:
    """
    Download schedule Image.
    """
    stage = crud.stage.get(db=db, id=stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    schedule = crud.schedule.get(db=db, stage_id=stage_id, stage=stage, teacher_id=None, room_id=None)

    url = get_stage_schedule_image(
        schedule=schedule,
        theme=Theme(
            colors=colors_theme[theme],
            directionality=directionality,
            language=language
        ),
    )
    return ImageUrl(url=url)
