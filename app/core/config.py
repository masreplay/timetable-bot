import secrets
from functools import lru_cache
from typing import List, Union

from dotenv import load_dotenv
from pydantic import BaseSettings, AnyHttpUrl, validator

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    HTML_TO_IMAGE_SERVICE: str
    TELEGRAM_BOT_API_TOKEN: str
    HEROKU_APP_NAME: str
    DATABASE_URL: str
    PORT: int
    TRANSLATION_KEY: str
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = "../../.env"
        case_sensitive = True


@lru_cache()
def settings():
    return Settings()


WEBHOOK_HOST = f'https://{settings().HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{settings().TELEGRAM_BOT_API_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = settings().PORT
