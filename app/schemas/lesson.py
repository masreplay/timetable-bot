from uuid import UUID

from sqlmodel import SQLModel, Field


# Shared properties
class LessonBase(SQLModel):
    subject_id: UUID = Field(default=None, foreign_key="subject.id")
    teacher_id: UUID | None = Field(default=None, foreign_key="user.id")
    stage_id: UUID | None = Field(default=None, foreign_key="stage.id")


class Lesson(LessonBase):
    id: UUID


# Properties to receive via API on creation
class LessonCreate(LessonBase):
    pass


# Properties to receive via API on update
class LessonUpdate(LessonBase):
    pass
