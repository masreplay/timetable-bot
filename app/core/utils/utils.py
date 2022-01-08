from typing import (
    Any,
    Sequence,
    Type,
)

from fastapi import APIRouter
from fastapi import params
from fastapi.datastructures import Default
from sqlmodel import SQLModel, Field
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute

from app.api.deps import PermissionHandler


def get_operation_from_method(method: str) -> str:
    if method == "GET":
        return "r"

    if method == "POST":
        return "c"

    if method == "PUT":
        return "u"

    if method == "DELETE":
        return "d"


class Permission(SQLModel):
    read: bool = Field()
    create: bool = Field()
    update: bool = Field()
    delete: bool = Field()


class APIPermissionsRouter(APIRouter):
    def include_permissions_router(
            self: APIRouter,
            router: "APIRouter" = None,
            prefix_permissions: str = "",
            tags: list[str] = None,
            dependencies: Sequence[params.Depends] | None = None,
            default_response_class: Type[Response] = Default(JSONResponse),
            responses: dict[int | str, dict[str, Any]] | None = None,
            callbacks: list[BaseRoute] | None = None,
            deprecated: bool | None = None,
            include_in_schema: bool = True,
    ):
        """
        Extension function (AKA monkey patching) on APIRouter to easily add permissions
        """
        _dependencies = [params.Depends(PermissionHandler(prefix_permissions))]
        if dependencies:
            _dependencies = _dependencies.extend(list(dependencies))

        self.include_router(router=router, prefix=f"/{prefix_permissions}", tags=tags, dependencies=_dependencies,
                            default_response_class=default_response_class, responses=responses, callbacks=callbacks,
                            deprecated=deprecated, include_in_schema=include_in_schema)
