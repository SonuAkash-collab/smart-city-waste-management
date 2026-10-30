"""Common API error handling.

Every error leaves the API in one shape, as agreed in SAD section 4.4:

    {"error": {"code": "STRING_CODE", "message": "Readable message"}}
"""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("scw.errors")

DEFAULT_CODES = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    422: "VALIDATION_ERROR",
    500: "INTERNAL_ERROR",
}


class ApiError(Exception):
    """An error that maps straight to an HTTP status and error code."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.headers = headers


def error_body(code: str, message: str, details: list | None = None) -> dict:
    """Build the common error body."""
    body: dict = {"error": {"code": code, "message": message}}
    if details:
        body["error"]["details"] = details
    return body


def _validation_details(exc: RequestValidationError) -> list[dict]:
    details = []
    for err in exc.errors():
        location = [str(part) for part in err.get("loc", ()) if part != "body"]
        details.append({"field": ".".join(location), "message": err.get("msg", "")})
    return details


def register_error_handlers(app: FastAPI) -> None:
    """Attach handlers so every error uses the common body."""

    @app.exception_handler(ApiError)
    async def handle_api_error(_: Request, exc: ApiError):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_body(exc.code, exc.message),
            headers=exc.headers,
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_error(_: Request, exc: StarletteHTTPException):
        code = DEFAULT_CODES.get(exc.status_code, "ERROR")
        message = exc.detail if isinstance(exc.detail, str) else code.replace("_", " ").capitalize()
        return JSONResponse(
            status_code=exc.status_code,
            content=error_body(code, message),
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError):
        details = _validation_details(exc)
        first = details[0] if details else {"field": "", "message": "Invalid input"}
        message = f"{first['field']}: {first['message']}" if first["field"] else first["message"]
        return JSONResponse(
            status_code=422,
            content=error_body("VALIDATION_ERROR", message, details),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception):
        logger.exception("Unhandled error", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content=error_body("INTERNAL_ERROR", "Something went wrong. Please try again."),
        )
