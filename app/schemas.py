from typing import Optional
from pydantic import BaseModel, Field


class TeacherPost(BaseModel):
    gmail: Optional[str] = Field(None, max_length=100, example="0000@gmail.com")
    name: Optional[str] = Field(None, max_length=35, example="بشار سعدون")
    is_supervisor: bool
    job_degree: Optional[str] = Field(None, example="دكتور")
    image_url: Optional[str] = Field(None)


class Teacher(BaseModel):
    job_degree: Optional[str] = Field(None, example="دكتور")
    image_url: Optional[str] = Field(None)
    id: str
    created_at: str
    updated_at: str = None
    deleted_at: str = None
    is_deleted: str
    gmail: Optional[str] = Field(None, max_length=100, example="0000@gmail.com")
    name: Optional[str] = Field(None, max_length=35, example="بشار سعدون")
    is_supervisor: bool
