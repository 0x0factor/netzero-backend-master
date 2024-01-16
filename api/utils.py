from functools import singledispatch
from types import SimpleNamespace
from typing import Callable

from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

from logger import get_logger


logger = get_logger(__name__)


@singledispatch
def wrap_namespace(ob):
    return ob


@wrap_namespace.register(dict)
def _wrap_dict(ob):
    return SimpleNamespace(**{k: wrap_namespace(v) for k, v in ob.items()})


@wrap_namespace.register(list)
def _wrap_list(ob):
    return [wrap_namespace(v) for v in ob]


class ErrorHandlerRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                # Default handler will handle this
                raise exc
            except HTTPException as exc:
                # Default handler will handle this
                raise exc
            except Exception as exc:
                logger.exception(f"Error occurred: {exc}")
                # Raise unknown exception
                raise exc

        return custom_route_handler
