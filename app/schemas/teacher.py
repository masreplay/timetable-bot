from app.routers.base_model import BaseSchema


class Teacher(BaseSchema, table=True):
    name: str
