from fastapi import HTTPException, Form


def form_data_to_list(items: list[str], data_type: type) -> list:
    print(f"itemsitemsitemsitemsitems{items}")
    try:
        if len(items) == 1 and items[0] == '':
            new_list = []
        elif len(items) == 1:
            new_list = items[0].split(",")
        else:
            new_list = []
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
