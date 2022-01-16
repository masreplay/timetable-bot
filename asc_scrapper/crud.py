import json
import pathlib
from functools import lru_cache
from typing import Type

from pydantic import parse_obj_as

from asc_scrapper import schemas
from asc_scrapper.schemas import *

T = TypeVar("T")


class AscCRUD:
    all = ["globals", "periods", "breaks", "bells", "daysdefs", "weeksdefs", "termsdefs", "days", "weeks", "terms",
           "buildings", "classrooms", "classes", "subjects", "teachers", "groups", "divisions", "students", "lessons",
           "studentsubjects", "cards", "ttreports", "classroomsupervisions", "coursegroups"]

    # asc type with its table
    included_dict: dict[type, str] = {
        schemas.Card: "cards",
        schemas.Day: "daysdefs",
        schemas.Subject: "subjects",
        schemas.Lesson: "lessons",
        schemas.Period: "periods",
        schemas.Teacher: "teachers",
        schemas.Class: "classes",
        schemas.Classroom: "classrooms",
        schemas.Building: "buildings",
    }

    # Wanted tables
    included = included_dict.values()

    # Unwanted tables
    ignores = set(all).difference(included)

    data: AscData

    def __init__(self, data: json):
        self.data = schemas.AscTimeTable.parse_obj(data).r.dbiAccessorRes

    @classmethod
    def from_file(cls, file_name: str):
        # FIXME
        """
        Get data from asc data json file
        :param file_name: json file name
        """
        json_file = open(file_name, encoding="utf8")
        data = json.load(json_file)
        return cls(data=data)

    # TODO: get data from asc website directly
    @classmethod
    def from_url(cls, url: str):
        raise NotImplementedError

    def get_table(self, type_: Type[T], *, name: str) -> list[T]:
        """
        Reusable parse table from asc by its name
        :param type_: schemas.Card
        :param name: any table name in wanted like "cards"
        :return: list of table values
        """
        assert name in self.included, "table not exist"
        for table in self.data.tables:
            if table.name == name:
                return parse_obj_as(list[type_], table.data_rows)

    @lru_cache
    def get_all(self, type_: Type[T]) -> list[T]:
        assert type_ in self.included_dict.keys(), "type not included"
        """
        Get table by its type from wanted_dict
        :param type_:
        :return:
        """
        return self.get_table(type_, name=self.included_dict[type_])

    def save_tables_as_files(self, *, dir_name: pathlib.Path = "asc_data"):
        """
        Save all wanted tables as files
        """
        pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)
        for column in self.data.tables:
            name = column.name
            if name in self.included:
                file = open(f"{dir_name}/{name}.json", "w", encoding="utf8")
                json.dump(column.dict(), file, indent=2, ensure_ascii=False)
                file.close()

    def get_item(self, *, id: str, type: Type[T]) -> T:
        """
        Reusable to get item by its id
        :param type: item type
        :param id: item id
        """
        table = self.get_all(type)
        for item in table:
            if item.id == id:
                return item

    def get_periods(self):
        return self.get_all(schemas.Period)

    def get_days(self):
        return self.get_all(schemas.Day)

    def get_classroom_schedule(self, classroom_id: str) -> Schedule:
        cards = self.get_all(schemas.Card)
        schedule = []
        for card in cards:
            classrooms: list = card.classroomids
            if len(classrooms) > 0 and classrooms[0] == classroom_id:
                schedule.append(card)

        return schedule

    def get_class_schedule(self, class_id: str) -> Schedule:
        cards = self.get_all(schemas.Card)
        schedule = []
        for card in cards:
            lesson = self.get_item(id=card.lessonid, type=schemas.Lesson)
            _class = self.get_item(id=lesson.class_id, type=schemas.Class)
            if _class and _class.id == class_id:
                schedule.append(card)
        return schedule

    def get__class_schedule_by_name(self, name: str) -> Schedule:
        """
        Get all class cards
        """
        cards = self.get_all(schemas.Card)
        schedule = []
        for card in cards:
            lesson = self.get_item(id=card.lessonid, type=schemas.Lesson)
            _class = self.get_item(id=lesson.class_id, type=schemas.Class)
            if _class and _class.name == name:
                schedule.append(card)
        return schedule

    def get_teacher_schedule(self, teacher_id: str) -> Schedule:
        """
        Get all teacher cards
        """
        cards = self.get_all(schemas.Card)
        schedule = []
        for card in cards:
            lesson = self.get_item(id=card.lessonid, type=schemas.Lesson)
            print(lesson)
            _class = self.get_item(id=lesson.teacher_id, type=schemas.Teacher)
            if _class and _class.id == teacher_id:
                schedule.append(card)
        return schedule

    def get_card(self, day: str, period: str, cards: list[Card]) -> schemas.Card | None:
        for card in cards:
            if card.period == period and card.days == day:
                return card


# if __name__ == '__main__':
#     crud: AscCRUD = AscCRUD.from_file(file_name="../asc_scrapper/asc_schedule.json")
#     crud.save_tables_as_files()
