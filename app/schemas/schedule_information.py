from datetime import date

from pydantic import BaseModel

from app.core.config import settings


class ScheduleInformation(BaseModel):
    validate_from: date
    validate_to: date

    collage_name: str
    branch_name: str

    creators_name: str

    creators_telegram_id: str
    creators_telegram_url: str

    bot_telegram_id: str
    bot_telegram_url: str


def get_schedule_information(
        validate_from: date,
        validate_to: date,
        collage_name: str,
        branch_name: str,
) -> ScheduleInformation:
    return ScheduleInformation(
        validate_from=validate_from,
        validate_to=validate_to,
        collage_name=collage_name,
        branch_name=branch_name,
        creators_name=settings().CREATORS_NAME,
        creators_telegram_id=settings().CREATORS_TELEGRAM_ID,
        creators_telegram_url=settings().BOT_TELEGRAM_URL,
        bot_telegram_id=settings().BOT_TELEGRAM_ID,
        bot_telegram_url=settings().BOT_TELEGRAM_URL,
    )
