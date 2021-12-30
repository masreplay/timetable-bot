from sqlmodel import SQLModel, Field


def get_operation_from_method(method: str) -> str:
    if method == "GET":
        return "r"

    if method == "POST":
        return "c"

    if method == "PUT":
        return "u"

    if method == "DELETE":
        return "d"


class Permission(SQLModel):
    read: bool = Field()
    create: bool = Field()
    update: bool = Field()
    delete: bool = Field()
