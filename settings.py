from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    html_to_image_service: str
    telegram_bot_api_token: str
    heroku_app_name: str
    database_url: str
    port: int
    translation_key: str

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()


WEBHOOK_HOST = f'https://{get_settings().heroku_app_name}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{get_settings().telegram_bot_api_token}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = get_settings().port
