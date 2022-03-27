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

default_per_page = 14


def get_stages(branch_id: str) -> schemas.Paging[schemas.Stage]:
    response = session.get(
        url=f"{settings().FAST_API_HOST}/stages",
        params=dict(branch_id=branch_id),
    )

    return schemas.Paging[schemas.Stage].parse_obj(response.json())


def get_branches() -> list[schemas.Branch]:
    response = session.get(url=f"{settings().FAST_API_HOST}/branches")
    return schemas.Paging[schemas.Branch].parse_obj(response.json()).results


def get_teachers(page: int, per_page: int = 15) -> schemas.Paging[schemas.User]:
    response = session.get(url=f"{settings().FAST_API_HOST}/users?page={page}&per_page={per_page}")
    return schemas.Paging[schemas.User].parse_obj(response.json())


def get_rooms(page: int, per_page: int = 15) -> schemas.Paging[schemas.Room]:
    response = session.get(url=f"{settings().FAST_API_HOST}/rooms?page={page}&per_page={per_page}")
    return schemas.Paging[schemas.Room].parse_obj(response.json())


def get_subjects(page: int, per_page: int = 15) -> schemas.Paging[schemas.Subject]:
    response = session.get(url=f"{settings().FAST_API_HOST}/subjects?page={page}&per_page={per_page}")
    return schemas.Paging[schemas.Subject].parse_obj(response.json())


def get_stages_schedules_images() -> list[ImageUrl]:
    response = session.get(url=f"{settings().FAST_API_HOST}/branches")
    return [
        ImageUrl(name="برمجيات ثاني صباحي",
                 url="https://masreplay.s3.amazonaws.com/fa3a06cf-6e00-41bb-a113-9c3ac47b89a4"),
        ImageUrl(name="وسائط ثاني مسائي",
                 url="https://masreplay.s3.amazonaws.com/fa3a06cf-6e00-41bb-a113-9c3ac47b89a4"),
        ImageUrl(name="برمجيات ثالث صباحي",
                 url="https://masreplay.s3.amazonaws.com/fa3a06cf-6e00-41bb-a113-9c3ac47b89a4"),
        ImageUrl(name="امنية ثاني مسائي",
                 url="https://masreplay.s3.amazonaws.com/fa3a06cf-6e00-41bb-a113-9c3ac47b89a4"),

    ]


def create_user(user: schemas.TelegramUserCreate):
    response = session.post(url=f"{settings().FAST_API_HOST}/telegram", json=user.dict())
    print(response.url)


def get_schedule_image_url(
        stage_id: UUID | None = None,
        teacher_id: UUID | None = None,
        classroom_id: UUID | None = None,
        subject_id: UUID | None = None,
):
    return session.get(
        url=f"{settings().FAST_API_HOST}/schedule/image",
        params=dict(
            stage_id=stage_id,
            teacher_id=teacher_id,
            classroom_id=classroom_id,
            subject_id=subject_id,
        )
    )


def get_stage_by_name(*, branch_name: str, stage_name: str) -> schemas.Stage | None:
    stages = get_stages(branch_name).results
    return next(filter(lambda stage: stage.name == stage_name, stages), None)


def get_stage_schedule(stage_id: UUID):
    return session.get(url=f"{settings().FAST_API_HOST}/schedule/stage/{stage_id}")
