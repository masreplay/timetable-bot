from typing import List, Any, Dict, Optional, Type

from pydantic import BaseModel, Field


class AscCard(BaseModel):
    id: str
    lessonid: str
    period: str
    days: str
    weeks: str
    classroomids: List[str]


Schedule: Type = list[AscCard]


class AscDay(BaseModel):
    id: str
    name: str
    short: str
    typ: str
    vals: List[str]
    val: Optional[int]


class AscSubject(BaseModel):
    id: str
    name: str
    short: str
    color: str
    picture_url: str
    timeoff: List[List[List[str]]]
    contract_weight: int


class AscLesson(BaseModel):
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


class AscPeriod(BaseModel):
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


class AscTeacher(BaseModel):
    id: str
    short: str
    gender: str
    bell: str
    color: str
    fontcolorprint: str
    fontcolorprint2: str
    fontcolorscreen: str
    timeoff: List[List[List[str]]]

    @property
    def get_name(self) -> Optional[str]:
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
    def first_name(self):
        if self.get_name:
            return self.get_name.split()[0]

    @property
    def second_name(self):
        if self.get_name:
            return self.get_name.split()[1]


class AscClass(BaseModel):
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


class AscClassroom(BaseModel):
    id: str
    name: str
    short: str
    buildingid: str
    sharedroom: bool
    needssupervision: bool
    color: str
    nearbyclassroomids: List
