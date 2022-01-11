import json
import pathlib
from typing import TypeVar, Type

from pydantic import parse_obj_as

from asc_scrapper import schemas
from asc_scrapper.schemas import AscData

T = TypeVar("T")


class AscCRUD:
    all = ["globals", "periods", "breaks", "bells", "daysdefs", "weeksdefs", "termsdefs", "days", "weeks", "terms",
           "buildings", "classrooms", "classes", "subjects", "teachers", "groups", "divisions", "students", "lessons",
           "studentsubjects", "cards", "ttreports", "classroomsupervisions", "coursegroups"]

    wanted = {"cards", "daysdefs", "subjects", "lessons", "periods", "teachers", "classes", "classrooms", "buildings"}

    ignores = set(all).difference(wanted)

    data: AscData

    def __init__(self, data: json):
        self.data = schemas.AscTimeTable.parse_obj(data).r.dbiAccessorRes

    # self.parse_table(schemas.Card, name="cards")
    def parse_table(self, type_: Type[T], *, name: str) -> list[T]:
        """
        parse table from asc by its name
        """
        assert name in self.wanted, "table not exist"
        for table in self.data.tables:
            if table.name == name:
                return parse_obj_as(list[type_], table.data_rows)

    def save_tables_as_files(self, *, dir_name: str = "/asc_data"):
        """
        save all wanted tables as files
        """
        pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)
        for column in self.data.tables:
            name = column.name
            if name in self.wanted:
                file = open(f"{dir_name}/{name}.json", "w", encoding="utf8")
                json.dump(column.dict(), file, indent=2, ensure_ascii=False)
                file.close()


if __name__ == '__main__':
    json_file = open(f"asc_schedule.json", encoding="utf8")
    data = json.load(json_file)

    asc_crud = AscCRUD(data=data)
    asc_crud.save_tables_as_files()
