import logging

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse

logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> PlainTextResponse:
    logger.warning(
        "validation_failed method=%s path=%s errors=%s",
        request.method,
        request.url.path,
        exc.errors(),
    )
    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"
    return PlainTextResponse(message, status_code=400)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "unhandled_exception method=%s path=%s",
        request.method,
        request.url.path,
    )
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
