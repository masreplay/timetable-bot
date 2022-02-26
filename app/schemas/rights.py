from pydantic import BaseModel


class Rights(BaseModel):
    teacher: bool = True
    subject: bool = True
    class_room: bool = True
    stage: bool = True
