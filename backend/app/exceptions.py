from fastapi.exceptions import RequestValidationError
from starlette.responses import PlainTextResponse

async def validation_exception_handler(request, exc: RequestValidationError) -> PlainTextResponse:
    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"
    return PlainTextResponse(message, status_code=400)
