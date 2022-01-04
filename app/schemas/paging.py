from typing import TypeVar, List, Generic

from fastapi import Query
from pydantic.generics import GenericModel
from sqlmodel import SQLModel


class LimitSkipParams(SQLModel):
    skip: int = Query(0, ge=0, description="Page skip")
    limit: int = Query(50, ge=1, le=100, description="Page size limit")


ModelType = TypeVar('ModelType')


class Paging(GenericModel, Generic[ModelType]):
    count: int
    results: List[ModelType]
