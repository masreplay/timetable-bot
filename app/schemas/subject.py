from uuid import UUID

from app.schemas.base import CardContent


# Shared properties


class SubjectBase(CardContent):
    pass


class Subject(SubjectBase):
    id: UUID


# Properties to receive via API on creation
class SubjectCreate(SubjectBase):
    pass


# Properties to receive via API on update
class SubjectUpdate(SubjectBase):
    pass
