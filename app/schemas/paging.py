from typing import TypeVar, Generic

from fastapi import Query
from pydantic import BaseModel
from pydantic.generics import GenericModel


class LimitSkipParams(BaseModel):
    skip: int = Query(0, ge=0)
    limit: int = Query(50, ge=1, le=100)


ModelType = TypeVar('ModelType')


class Paging(GenericModel, Generic[ModelType]):
    count: int
    results: list[ModelType]

    class Config:
        orm_mode = True
