import requests

from app import schemas
from app.core.config import settings


def get_stages(branch_name: str):
    response = requests.get(url=f"{settings().FAST_API_HOST}/stages?branch_name={branch_name}")
    return schemas.Paging[schemas.Stage].parse_obj(response.json()).results
