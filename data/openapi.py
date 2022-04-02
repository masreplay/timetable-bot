import json
from pathlib import Path

import requests

from app.core.config import settings


def format_openapi_file():
    version = "v1"
    response = requests.get(f"{settings().FAST_API_HOST}/openapi.json")

    if response.status_code == 200:
        openapi_path = Path("openapi-formatted.json")

        openapi_content = response.json()
        for path_data in openapi_content["paths"].values():
            for operation in path_data.values():
                try:
                    tag = operation["tags"][0]
                    operation_id = operation["operationId"].replace(f"{version}_", "")
                    to_remove = f"{tag}-"
                    new_operation_id = operation_id[len(to_remove):]
                    operation["operationId"] = new_operation_id
                except Exception as e:
                    print(f"error {e}")

        openapi_path.write_text(json.dumps(openapi_content))
