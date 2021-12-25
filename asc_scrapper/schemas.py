from typing import List, Any, Dict, Optional, Type

from pydantic import BaseModel


class Card(BaseModel):
    id: str
    lessonid: str
    period: str
    days: str
    weeks: str
    classroomids: List[str]


Schedule: Type = list[Card]


class Day(BaseModel):
    id: str
    name: str
    short: str
    typ: str
    vals: List[str]
    val: Optional[int]


class Subject(BaseModel):
    id: str
    name: str
    short: str
    color: str
    picture_url: str
    timeoff: List[List[List[str]]]
    contract_weight: int


class Lesson(BaseModel):
    id: str
    subjectid: str
    teacherids: List[str]
    groupids: List[str]
    classids: List[str]
    count: int
    durationperiods: int
    classroomidss: List[List[str]]
    termsdefid: str
    weeksdefid: str
    daysdefid: str
    terms: str
    seminargroup: Any
    bell: str
    studentids: List
    groupnames: List[str]


class Period(BaseModel):
    id: str
    period: str
    name: str
    short: str
    starttime: str
    endtime: str
    daydata: Dict[str, Any]
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
    timeoff: List[List[List[str]]]


class Class(BaseModel):
    id: str
    name: str
    short: str
    teacherid: str
    classroomids: List[str]
    bell: str
    color: str
    timeoff: List[List[List[str]]]
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
    nearbyclassroomids: List