import uuid

from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, \
    InlineQueryResultPhoto

from app import schemas
from bot_app import service
from bot_app.main import dp, bot


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    text = inline_query.query
    if "teacher" in text or "استاذ" in text:
        teachers: list[schemas.User] = []

        items = []
        for teacher in teachers:
            items.append(
                InlineQueryResultArticle(
                    id=str(teacher.id),
                    title=teacher.name,
                    input_message_content=InputTextMessageContent(f"m. {teacher.name}"),
                )
            )
        # don't forget to set cache_time=1 for testing (default is 300s or 5m)
        await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)
    else:
        images = service.get_stages_schedules_images()

        items = [
            InlineQueryResultPhoto(
                id=str(uuid.uuid4()),
                title=f'Result {text!r}',
                caption=image.name,
                photo_url=image.url,
                thumb_url=image.url,
            )
            for image in images
        ]

        # don't forget to set cache_time=1 for testing (default is 300s or 5m)
        await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)
