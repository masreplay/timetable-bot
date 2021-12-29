import logging

from fastapi import FastAPI
from fastapi.logger import logger
from starlette.middleware.cors import CORSMiddleware

from app.routers import users

app = FastAPI(
    title="Installmensts App",
    version="1",
)

app.include_router(users.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:52120",
    "https://installment-web.herokuapp.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")

uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
logger.handlers = gunicorn_error_logger.handlers

if __name__ != "__main__":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)
