from contextlib import asynccontextmanager
import logging
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.exceptions import validation_exception_handler, unhandled_exception_handler
from app.logging_config import configure_logging
from app.routers.benchmark import router as benchmark_router
from db import init_db

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("server_starting")
    logger.info("db_schema_initialization_started")
    await init_db()
    logger.info("db_schema_initialization_completed")

    yield

    logger.info("server_shutting_down")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    logger.info("request_started method=%s path=%s", request.method, request.url.path)
    response = await call_next(request)
    status_code = response.status_code
    if status_code >= 500:
        logger.error(
            "request_completed_with_server_error method=%s path=%s status=%s",
            request.method,
            request.url.path,
            status_code,
        )
    elif status_code >= 400:
        logger.warning(
            "request_completed_with_client_error method=%s path=%s status=%s",
            request.method,
            request.url.path,
            status_code,
        )
    else:
        logger.info(
            "request_completed_successfully method=%s path=%s status=%s",
            request.method,
            request.url.path,
            status_code,
        )
    return response

app.include_router(benchmark_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
