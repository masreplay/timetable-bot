import secrets
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, AnyHttpUrl, validator, EmailStr, root_validator

from app.schemas.enums import Environment

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URL: str
    TRANSLATION_KEY: str

    CREATORS_NAME: str 
    CREATORS_TELEGRAM_ID: str
    CREATORS_TELEGRAM_URL: str
    BOT_TELEGRAM_ID: str
    BOT_TELEGRAM_URL: str

    RESPONSIBLE_USERS: list[EmailStr] = []

    @validator("RESPONSIBLE_USERS", pre=True)
    def assemble_emails(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = "../../.env"
        case_sensitive = True

    HTML_TO_IMAGE_SERVICE: str

    TELEGRAM_BOT_API_TOKEN: str
    FRONTEND_URL: str

    # webserver settings
    WEBAPP_HOST = '0.0.0.0'
    PORT: int

    HEROKU_APP_NAME: str

    ENVIRONMENT: Environment

    @validator("ENVIRONMENT", pre=True)
    def cast_environment(cls, v: str | None) -> Environment:
        if v:
            # get enum by its enum representation
            return Environment[v]
        else:
            return Environment.development

    HEROKU_APP_HOST: str

    @root_validator(pre=True)
    def assemble_app_host(cls, values):
        new = dict(values)
        name = new.get('HEROKU_APP_NAME')
        new['HEROKU_APP_HOST'] = f'https://{name}.herokuapp.com'
        return new

    FAST_API_HOST: str

    @root_validator(pre=True)
    def assemble_fast_api_host(cls, values):
        new = dict(values)
        environment: Environment = new.get('ENVIRONMENT')
        version = "/v1"

        if environment == Environment.development:
            new['FAST_API_HOST'] = f"http://127.0.0.1:8000{version}"
            return new

        else:
            host = new.get('HEROKU_APP_HOST')
            new['FAST_API_HOST'] = f'{host}{version}'
            return new

    WEBHOOK_PATH: str

    @root_validator(pre=True)
    def assemble_webhook_path(cls, values):
        new = dict(values)
        new['WEBHOOK_PATH'] = f'/webhook/{new.get("TELEGRAM_BOT_API_TOKEN")}'
        return new

    WEBHOOK_URL: str

    @root_validator(pre=True)
    def assemble_webhook_url(cls, values):
        new = dict(values)

        new['WEBHOOK_URL'] = f'{new.get("HEROKU_APP_HOST")}{new.get("WEBHOOK_PATH")}'
        return new


@lru_cache()
def settings():
    return Settings()
