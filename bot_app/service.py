from uuid import UUID

import requests

from app import schemas
from app.core.config import settings


# Fixme: implement error handler and handel base url as subclass from requests.Session

def get_stages(branch_name: str) -> schemas.Paging[schemas.Stage]:
    response = requests.get(url=f"{settings().FAST_API_HOST}/stages?branch_name={branch_name}")
    return schemas.Paging[schemas.Stage].parse_obj(response.json())


def get_stage_by_name(*, branch_name: str, stage_name: str) -> schemas.Stage | None:
    stages = get_stages(branch_name).results
    return next(filter(lambda stage: stage.name == stage_name, stages), None)


def get_stage_schedule(stage_id: UUID):
    return requests.get(url=f"{settings().FAST_API_HOST}/schedule/stage/{stage_id}")
