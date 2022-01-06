from typing import Optional, Type

from pydantic import Field, BaseModel


class UotTeacher(BaseModel):
    id: str
    ar_name: Optional[str]
    en_name: str
    image: str
    stages_id: list[str] = Field([])
    email: Optional[str]
    uot_url: str
    role_id: Optional[str]

    @property
    def first_name(self):
        return self.ar_name.split()[0]

    @property
    def second_name(self):
        return self.ar_name.split()[1]


class UotRole(BaseModel):
    id: str
    en_name: str
    ar_name: Optional[str]


UotTeachers: Type = list[UotTeacher]
UotRoles: Type = list[UotRole]


class UotTeacherCreate(UotTeacher):
    pass


class UotTeacherEdit(UotTeacher):
    pass
