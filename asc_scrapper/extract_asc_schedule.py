import json
import os
from typing import Type, TypeVar

from pydantic import parse_obj_as

T = TypeVar('T')


def load_data(file_name: str, data_type: Type[T], data_rows: str = "data_rows") -> list[T]:
    with open(file_name, 'r', encoding="utf-8") as file:
        return parse_obj_as(list[data_type], json.load(file)[data_rows])


def main():
    json_file = open("asc_schedule.json", encoding="utf8")
    data = json.load(json_file, )

    os.chdir("asc_data")

    ignores = ["weeksdefs", "weeks", "termsdefs", "terms", "breaks", "studentsubjects", "students", "bells", ""]

    for i in data['asc_data']:
        name = i['id']
        if name not in ignores:
            file = open(f"{name}.json", "w", encoding="utf8")
            i.pop('cdefs', None)
            i.pop('def', None)
            json.dump(i, file, indent=2, ensure_ascii=False)
            file.close()


if __name__ == '__main__':
    main()
