from uuid import UUID

import requests

from app import schemas
from app.core.config import settings

# Fixme: implement error handler and handel base url as subclass from requests.Session
from asc_scrapper.test import ImageUrl


def get_stages(branch_name: str) -> schemas.Paging[schemas.Stage]:
    response = requests.get(
        url=f"{settings().FAST_API_HOST}/stages",
        params=dict(branch_name=branch_name),
    )

    return schemas.Paging[schemas.Stage].parse_obj(response.json())


def get_schedule_image_url(stage_id: UUID) -> str:
    response = requests.get(
        url=f"{settings().FAST_API_HOST}/schedule/image",
        params={"stage_id": stage_id}
    )
    print("testablity"+ImageUrl.parse_obj(response.json()).url)
    return ImageUrl.parse_obj(response.json()).url


def get_stage_by_name(*, branch_name: str, stage_name: str) -> schemas.Stage | None:
    stages = get_stages(branch_name).results
    return next(filter(lambda stage: stage.name == stage_name, stages), None)


def get_stage_schedule(stage_id: UUID):
    return requests.get(url=f"{settings().FAST_API_HOST}/schedule/stage/{stage_id}")
