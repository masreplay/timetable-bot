from typing import Any

from pydantic import BaseModel, Field


class AscItem(BaseModel):
    name: str = Field(alias="id")
    data_rows: list[dict]


class AscData(BaseModel):
    data: list[AscItem]


class Card(BaseModel):
    id: str
    lessonid: str
    period: str
    days: str
    weeks: str
    classroomids: list[str]


Schedule = list[Card]


class Day(BaseModel):
    id: str
    name: str
    short: str
    typ: str
    vals: list[str]
    val: int | None


class Subject(BaseModel):
    id: str
    name: str
    short: str
    color: str
    picture_url: str
    timeoff: list[list[list[str]]]
    contract_weight: int


class Lesson(BaseModel):
    id: str
    subjectid: str
    teacherids: list[str]
    groupids: list[str]
    classids: list[str]
    count: int
    durationperiods: int
    classroomidss: list[list[str]]
    termsdefid: str
    weeksdefid: str
    daysdefid: str
    terms: str
    seminargroup: Any
    bell: str
    studentids: list
    groupnames: list[str]


class Period(BaseModel):
    id: str
    period: str
    name: str
    short: str
    starttime: str
    endtime: str
    daydata: dict[str, Any]
    printinsummary: bool
    printinteacher: bool
    printinclass: bool
    printinclassroom: bool
    printonlyinbell: str

    @property
    def time(self):
        return f"{self.starttime} - {self.endtime}"


class Teacher(BaseModel):
    id: str
    short: str
    gender: str
    bell: str
    color: str
    fontcolorprint: str
    fontcolorprint2: str
    fontcolorscreen: str
    timeoff: list[list[list[str]]]

    @property
    def get_name(self) -> str:
        """
        :return: name without job title
        """
        name = self.short.split(".")
        # remove where د.م.
        name = name[-1]
        if len(name) not in [0, 1]:
            # remove where د م ا or empty spaces
            separated_name = name.split(" ")
            for part in separated_name:
                if len(part) in [0, 1]:
                    separated_name.remove(part)
            return " ".join(separated_name)

    @property
    def job_title(self) -> str | None:
        try:
            job_title: str = self.short.split(self.get_name)[0].replace(" ", "")
        except IndexError:
            return ""

    @property
    def first_name(self):
        if self.get_name:
            return self.get_name.split()[0]

    @property
    def second_name(self):
        if self.get_name:
            return self.get_name.split()[1]


class Class(BaseModel):
    id: str
    name: str
    teacherid: str
    classroomids: list[str]
    bell: str
    color: str
    timeoff: list[list[list[str]]]
    printsubjectpictures: bool
    classroomid: str


class Classroom(BaseModel):
    id: str
    name: str
    short: str
    buildingid: str
    sharedroom: bool
    needssupervision: bool
    color: str
    nearbyclassroomids: list


class Building(BaseModel):
    id: str
    name: str
    short: str
    color: str
