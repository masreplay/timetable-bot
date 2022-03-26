from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.image_url import ImageUrl
from app.schemas.schedule import ScheduleDetails
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
        stage_id: UUID | None = None,
        teacher_id: UUID | None = None,
        classroom_id: UUID | None = None,
        subject_id: UUID | None = None,
        db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve Single schedule.
    """

    if stage_id:
        stage = crud.stage.get(db=db, id=stage_id)
        if not stage:
            raise HTTPException(status_code=404, detail="Stage not found")
        return crud.schedule.get_stage_schedule(db=db, stage=stage)
    elif teacher_id:
        teacher = crud.user.get(db=db, id=teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        return crud.schedule.get_teacher_schedule(db=db, teacher=teacher)
    elif classroom_id:
        classroom = crud.room.get(db=db, id=classroom_id)
        if not classroom:
            raise HTTPException(status_code=404, detail="Classroom not found")
        return crud.schedule.get_classroom_schedule(db=db, classroom=classroom)
    elif subject_id:
        subject = crud.subject.get(db=db, id=subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        return crud.schedule.get_subject_schedule(db=db, subject=subject)
    else:
        return crud.schedule.default_stage_schedule(db=db)


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

    schedule = crud.schedule.get_stage_schedule(db=db, stage=stage)

    url = get_stage_schedule_image(
        schedule=schedule,
        theme=Theme(
            colors=colors_theme[theme],
            directionality=directionality,
            language=language
        ),
    )
    if url:
        return ImageUrl(
            url=url,
            name=schedule.item.name
        )
    else:
        raise HTTPException(status_code=400, detail="Error")
