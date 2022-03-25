import json
import shutil
from pathlib import Path

import requests

from app.core.config import settings


def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def generate_formatted_openapi():
    download_file(f"{settings().FAST_API_HOST}/openapi.json")

    file_path = Path("./openapi.json")
    openapi_content = json.loads(file_path.read_text())

    for path_data in openapi_content["paths"].values():
        for operation in path_data.values():
            tag = operation["tags"][0]
            operation_id = operation["operationId"]
            to_remove = f"{tag}-"
            new_operation_id = operation_id[len(to_remove):]
            operation["operationId"] = new_operation_id

    file_path.write_text(json.dumps(openapi_content, indent=2, ensure_ascii=False))
