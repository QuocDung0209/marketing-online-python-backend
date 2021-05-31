from typing import Any

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from app.core.error_handling.http_error import http_error_handler
from app.core.error_handling.validation_error import http422_error_handler


class ApplicationBase(FastAPI):
    def __init__(self, title: str, openapi_url: str, debug: bool, version: str):
        super().__init__(
            title=title, openapi_url=openapi_url, debug=debug, version=version
        )
        self.__setup_default_application__()

    def __setup_default_application__(self) -> Any:
        self.add_exception_handler(HTTPException, http_error_handler)
        self.add_exception_handler(RequestValidationError, http422_error_handler)
