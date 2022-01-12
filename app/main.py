import logging
import time

from fastapi import FastAPI, Request
from fastapi.logger import logger
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1 import api
from app.core.config import settings
from app.open_api_to_files.main import get_models_zip
from app.db.initial_db import main as seed_db

app = FastAPI(
    title="CS UOT App",
    version="1",
    openapi_url=f"{settings().API_V1_STR}/openapi.json",
    docs_url=f"{settings().API_V1_STR}/docs",
    redoc_url=f"{settings().API_V1_STR}/redoc",
)


@app.on_event("startup")
async def startup_event():
    seed_db()


# Routers
app.include_router(api.api_router, prefix=settings().API_V1_STR)


# Process time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Models to files
@app.get(f"{settings().API_V1_STR}/models", tags=["models"])
def get_all_models():
    return get_models_zip(app.routes)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings().BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")

uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
logger.handlers = gunicorn_error_logger.handlers

if __name__ != "__main__":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)
