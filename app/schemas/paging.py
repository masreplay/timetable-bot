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
