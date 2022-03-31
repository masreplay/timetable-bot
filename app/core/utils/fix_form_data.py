from fastapi import HTTPException, Form


def FormList(items: list[str], data_type: type):
    try:
        new_list = items[0].split(",") if len(items) == 1 else []
        return list[data_type](map(data_type, new_list))
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": [
                        "list"
                    ],
                    "msg": "error",
                    "type": f"list must be type of {data_type.__name__}"
                }
            ]
        )
