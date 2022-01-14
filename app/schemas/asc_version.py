from uuid import UUID

from sqlmodel import SQLModel, Field


# Shared properties
class AscVersionBase(SQLModel):
    created_by: UUID = Field(foreign_key="user.id")
    file_name: str


class AscVersion(AscVersionBase):
    id: UUID


# Properties to receive via API on creation
class AscVersionCreate(AscVersionBase):
    pass
