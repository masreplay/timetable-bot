from uuid import UUID

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from app import schemas
from app.core.config import settings
from app.schemas.image_url import ImageUrl

session = requests.Session()
session.trust_env = False
retry = Retry(connect=1, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)


def get_stages(branch_id: str) -> schemas.Paging[schemas.Stage]:
    response = session.get(
        url=f"{settings().FAST_API_HOST}/stages",
        params=dict(branch_id=branch_id),
    )

    return schemas.Paging[schemas.Stage].parse_obj(response.json())


def get_branches() -> list[schemas.Branch]:
    response = session.get(url=f"{settings().FAST_API_HOST}/branches")
    return schemas.Paging[schemas.Branch].parse_obj(response.json()).results


def create_user(user: schemas.TelegramUserCreate):
    response = session.post(url=f"{settings().FAST_API_HOST}/telegram", json=user.dict())
    print(response.url)


def get_schedule_image_url(stage_id: str) -> ImageUrl:
    response = session.get(
        url=f"{settings().FAST_API_HOST}/schedule/image",
        params=dict(stage_id=stage_id)
    )
    return ImageUrl.parse_obj(response.json())


def get_stage_by_name(*, branch_name: str, stage_name: str) -> schemas.Stage | None:
    stages = get_stages(branch_name).results
    return next(filter(lambda stage: stage.name == stage_name, stages), None)


def get_stage_schedule(stage_id: UUID):
    return session.get(url=f"{settings().FAST_API_HOST}/schedule/stage/{stage_id}")
