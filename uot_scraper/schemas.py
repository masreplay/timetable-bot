from typing import Optional, Type

from pydantic import Field, BaseModel


class Teacher(BaseModel):
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


class Role(BaseModel):
    id: str
    en_name: str
    ar_name: Optional[str]


Teachers: Type = list[Teacher]
Roles: Type = list[Role]


class TeacherCreate(Teacher):
    pass


class TeacherEdit(Teacher):
    pass
