# {
#       "id": "f7a00054-31b9-4c6b-a241-f2a4aa8e008a",
#       "ar_name": "علاء نوري مظهر",
#       "en_name": "Alaa Noori Mazhar",
#       "image": "https://cs.uotechnology.edu.iq/media/k2/items/cache/07758ee08f7e16a0b15b0d98a56d204a_XS.jpg",
#       "stage_id": [
#         ""
#       ],
#       "email": "110027@uotechnology.edu.iq",
#       "uot_url": "https://cs.uotechnology.edu.iq/index.php/s/cv/1252-alaa-noori-mazhar",
#       "role_id": "2e104deb-042e-426d-ad78-a557c73f45d2"
#     }
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
