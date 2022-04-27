from typing import TypeVar, Generic

from fastapi import Query
from pydantic import BaseModel
from pydantic.generics import GenericModel

ModelType = TypeVar('ModelType')


class Paging(GenericModel, Generic[ModelType]):
    count: int
    results: list[ModelType]

    class Config:
        orm_mode = True


class PagingParams(BaseModel):
    skip: int
    limit: int


def paging(page: int = Query(1, ge=1), per_page: int = Query(15)):
    return PagingParams(skip=page * per_page - per_page, limit=per_page)
