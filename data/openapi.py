import json
from pathlib import Path

file_path = Path("openapi.json")
openapi_content = json.loads(file_path.read_text())
version = "v1"
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

file_path.write_text(json.dumps(openapi_content))
