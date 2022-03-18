from uuid import UUID

import requests

from app import schemas
from app.core.config import settings

# Fixme: implement error handler and handel base url as subclass from requests.Session
from asc_scrapper.test import ImageUrl

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=1, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)


def get_stages(branch_name: str) -> schemas.Paging[schemas.Stage]:
    response = session.get(
        url=f"http://localhost/v1/stages",
        params=dict(branch_name=branch_name),
    )

    return schemas.Paging[schemas.Stage].parse_obj(response.json())


def get_branches() -> list[schemas.Branch]:
    response = session.get(url=f"http://localhost/v1/branches")
    print("testofalltest" + response.url)
    return schemas.Paging[schemas.Branch].parse_obj(response.json()).results


def get_schedule_image_url(stage_id: UUID) -> str:
    response = session.get(
        url=f"http://localhost/v1/schedule/image",
        params=dict(stage_id=stage_id)
    )
    print("testablity" + ImageUrl.parse_obj(response.json()).url)
    return ImageUrl.parse_obj(response.json()).url


def get_stage_by_name(*, branch_name: str, stage_name: str) -> schemas.Stage | None:
    stages = get_stages(branch_name).results
    return next(filter(lambda stage: stage.name == stage_name, stages), None)


def get_stage_schedule(stage_id: UUID):
    return session.get(url=f"http://localhost/v1/schedule/stage/{stage_id}")
