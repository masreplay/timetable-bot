from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field


# Shared properties
class LessonBase(SQLModel):
    subject_id: UUID = Field(default=None, foreign_key="subject.id")
    teacher_id: Optional[UUID] = Field(default=None, foreign_key="teacher.id")
    class_id: Optional[UUID] = Field(default=None, foreign_key="class.id")


class Lesson(LessonBase):
    id: UUID


# Properties to receive via API on creation
class LessonCreate(LessonBase):
    pass


# Properties to receive via API on update
class LessonUpdate(LessonBase):
    pass
