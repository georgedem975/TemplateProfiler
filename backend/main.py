from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.exceptions import validation_exception_handler
from app.routers.benchmark import router as benchmark_router
from db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("Application starting up...")
    print("init db schema...")
    await init_db()

    yield

    print("Application shutting down...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(benchmark_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
