import inspect
from typing import Type

from fastapi import FastAPI, Form
from pydantic import BaseModel
from pydantic.fields import ModelField

app = FastAPI()


def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    # field.type_ is list[str]:
    # Unfortunately pydantic doesn't pass array as list but as str!
    # https://github.com/tiangolo/fastapi/issues/318

    new_params = []
    for field in cls.__fields__.values():
        param = inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
        )
        new_params.append(param)

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls

# @as_form
# class Item(BaseModel):
#     name: str
#     another: str
#     opts: Json[Dict[str, int]] = '{}'
#
#
# @app.post("/test")
# async def endpoint(item: Item = Depends(Item.as_form)):
#     return item.dict()
