import json
import pathlib
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

    def get_all(self, type_: Type[T]):
        assert type_ in self.included_dict.keys(), "type not included"
        """
        Get table by its type from wanted_dict
        :param type_:
        :return:
        """
        self.get_table(type_, name=self.included_dict[type_])

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

    def get_item_by_id(self, *, id: str, table_name: str) -> T:
        """
        Reusable to get item by its id
        :param id: item id
        :param table_name: table name from asc wanted json
        """
        table = self.get_table(schemas.Teacher, name=table_name)
        for item in table:
            if item.id == id:
                return item

    def get_periods(self):
        return self.get_table(schemas.Period, name="periods")

    def get_days(self):
        return self.get_table(schemas.Day, name="days")

    def get_classroom_schedule(self, classroom_id: str) -> Schedule:
        cards = self.get_table(schemas.Card, name="cards")
        schedule = []
        for card in cards:
            classrooms: list = card.classroomids
            if len(classrooms) > 0 and classrooms[0] == classroom_id:
                schedule.append(card)

        return schedule

    def get_class_schedule(self, class_id: str) -> Schedule:
        cards = self.get_table(schemas.Card, name="cards")
        schedule = []
        for card in cards:
            _class = self.get_class_by_lesson_id(card.lessonid)
            if _class and _class.id == class_id:
                schedule.append(card)
        return schedule

    def get_schedule_by_class_name(self, name: str) -> Schedule:
        cards = self.get_table(schemas.Card, name="cards")
        schedule = []
        for card in cards:
            _class = self.get_class_by_lesson_id(card.lessonid)
            if _class and _class.name == name:
                schedule.append(card)
        return schedule

    def get_teacher_schedule(self, teacher_id: str) -> Schedule:
        cards = self.get_table(schemas.Card, name="cards")
        schedule = []
        for card in cards:
            _class = self.get_teacher_by_lesson_id(card.lessonid)
            if _class and _class.id == teacher_id:
                schedule.append(card)
        return schedule

    def get_card(self, day: str, period: str) -> schemas.Card | None:
        cards = self.get_table(schemas.Card, name="cards")
        for card in cards:
            if card.period == period and card.days == day:
                return card

    def get_subject_by_lesson_id(self, lesson_id: str) -> schemas.Subject:
        lesson = self.get_item_by_id(id=lesson_id, table_name="lessons")
        return self.get_item_by_id(id=lesson.subjectid, table_name="subjects")

    def get_classroom_by_lesson_id(self, lesson_id: str) -> schemas.Classroom:
        lesson = self.get_item_by_id(id=lesson_id, table_name="lessons")
        return self.get_item_by_id(id=lesson.classroomidss[0][0], table_name="classrooms")

    def get_class_by_lesson_id(self, lesson_id: str) -> schemas.Class:
        lesson = self.get_item_by_id(id=lesson_id, table_name="lessons")
        classes = lesson.classids
        if len(classes) > 0:
            return self.get_item_by_id(id=classes[0], table_name="classs")

    def get_teacher_by_lesson_id(self, lesson_id: str) -> schemas.Teacher:
        lesson = self.get_item_by_id(id=lesson_id, table_name="lessons")
        teachers = lesson.teacherids
        if len(teachers) > 0:
            return self.get_item_by_id(id=teachers[0], table_name="teachers")


if __name__ == '__main__':
    asc_crud = AscCRUD.from_file(file_name="asc_schedule.json")

    asc_crud.save_tables_as_files()
