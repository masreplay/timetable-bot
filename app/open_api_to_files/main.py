import zipfile

from enum import Enum
from io import BytesIO
from typing import Sequence

from fastapi.openapi.utils import get_flat_models_from_routes
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from starlette.routing import BaseRoute

from app.open_api_to_files.pydantic_to_class import DartConvertor, ClassFile


def get_models_zip(routes: Sequence[BaseRoute]):
    models = get_flat_models_from_routes(routes)
    classes = [c for c in models if issubclass(c, BaseModel)]
    enums = [e for e in models if issubclass(e, Enum)]
    return zip_files(
        classes=[DartConvertor(c).file for c in classes],
        enums=[DartConvertor.enum(e) for e in enums]
    )


def zip_files(classes: list[ClassFile], enums: list[ClassFile]):
    zipped_file = BytesIO()
    with zipfile.ZipFile(zipped_file, 'a', zipfile.ZIP_DEFLATED) as zipped:
        main_dir = "models/"
        for c in classes:
            zipped.writestr(f"{main_dir}{c.name}", c.body)
        for e in enums:
            zipped.writestr(f"{main_dir}{e.name}", e.body)
    zipped_file.seek(0)
    response = StreamingResponse(zipped_file, media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = "attachment; filename=models.zip"
    return response
