from fastapi import APIRouter

from app.api.api_v1.tags import Tags
from app.open_api_to_files.main import get_models_zip

router = APIRouter()


# Models to files
@router.get(f"/", tags=[Tags.models])
def get_all_models():
    return get_models_zip(router.routes)
