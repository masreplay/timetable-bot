import logging
import uuid
from enum import Enum

import aiogram.utils.markdown as md
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, CallbackQuery, InlineQuery, InputTextMessageContent, InlineQueryResultArticle, \
    InlineQueryResultPhoto
from aiogram.utils.executor import start_webhook

from app import crud, schemas
from app.core.config import settings
from app.db.db import get_db
from app.schemas.enums import UserType
from asc_scrapper.test import get_schedule_image
from i18n import translate

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings().TELEGRAM_BOT_API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


# States
class Form(StatesGroup):
    branch = State()
    stage = State()


class Commands(str, Enum):
    start = "start"
    schedule = "schedule"
    cancel = "cancel"


@dp.message_handler(commands=Commands.start)
async def cmd_schedule(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    markup.add("مرحلة دراسية 🏬")
    markup.add("استاذ 🧑‍🏫")
    markup.add("مادة 📔")
    await Form.next()
    await message.reply("اختر نوع الجدول", reply_markup=markup)


@dp.message_handler(commands=Commands.schedule)
async def cmd_schedule(message: types.Message):
    """
    Get branch
    """
    # Set state
    await Form.branch.set()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    response = requests.get(url=f"{settings().FAST_API_HOST}/branches")
    items = schemas.Paging[schemas.Branch].parse_obj(response.json()).results

    for i in range(0, len(items), 2):
        try:
            markup.add(items[i].name, items[i + 1].name)
        except IndexError:
            markup.add(items[i].name)

    await message.reply(f"اختر الفرع", reply_markup=markup)


@dp.message_handler(state=Form.branch)
async def process_branch(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    response = requests.get(url=f"{settings().FAST_API_HOST}/stages?branch_name={message.text}")
    items = schemas.Paging[schemas.Stage].parse_obj(response.json()).results
    for item in items:
        markup.add(item.name)

    await message.reply("اختر المرحلة", reply_markup=markup)
    await Form.next()


@dp.message_handler(state=Form.stage)
async def process_stage(message: types.Message, state: FSMContext):
    await state.update_data(stage=str(message.text))
    await message.reply('...جاري تحويل الصورة', reply_markup=types.ReplyKeyboardRemove())

    # Remove keyboard
    markup = types.ReplyKeyboardRemove()

    name = f'{message.text}'

    url = get_schedule_image(name)
    print(f"{url}")
    # And send message
    await bot.send_photo(
        chat_id=message.chat.id,
        caption=md.text(
            md.text(f"جدول: {md.link(name, 'https://uot.csschedule.app/stage/123-123-123-123')}"),
            sep='\n',
        ),
        photo=url,
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )

    # Finish conversation

    await state.finish()


@dp.message_handler(commands='teachers')
async def cmd_schedule(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    await message.reply("استاذة القسم؟", reply_markup=markup)


@dp.message_handler(commands='about')
async def cmd_about(message: types.Message):
    buttons = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)

    buttons.add(types.InlineKeyboardButton('منو سوة هذا الاختراع؟', callback_data='credits'))
    buttons.add(types.InlineKeyboardButton('شنو الطريقة السوينا بيها؟', callback_data='technologies'))
    buttons.add(types.InlineKeyboardButton('شلون يشتغل؟', callback_data='how_does_it_work'))

    await bot.send_message(
        chat_id=message.chat.id,
        text=md.text(translate("ar", "about")),
        reply_markup=buttons,
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.callback_query_handler(lambda c: c.data == 'credits')
async def process_credits(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    await bot.edit_message_text(
        text=md.text(translate("ar", "credits")),
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
    )


@dp.callback_query_handler(lambda c: c.data == 'technologies')
async def process_technologies(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    await bot.edit_message_text(
        text=md.text(translate("ar", "technologies")),
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.callback_query_handler(lambda c: c.data == 'how_does_it_work')
async def process_credits(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    await bot.edit_message_text(
        text=md.text(translate("ar", "how_does_it_work")),
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    # id affects both preview and content,
    # so it has to be unique for each result
    # (Unique identifier for this result, 1-64 Bytes)
    # you can set your unique id's
    # but for example i'll generate it based on text because I know, that
    # only text will be passed in this example
    text = inline_query.query
    if text.__contains__("teacher") or text.__contains__("استاذ"):
        with next(get_db()) as db:
            teachers: list[schemas.User] = crud.user.get_filter(db=db, query=text, role_id=None,
                                                                user_type=UserType.teacher, )

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

        item = InlineQueryResultPhoto(
            id=str(uuid.uuid4()),
            title=f'Result {text!r}',
            caption="جدول فارغ",
            # input_message_content=input_content,
            photo_url="https://masreplay.s3.amazonaws.com/fa3a06cf-6e00-41bb-a113-9c3ac47b89a4",
            thumb_url="https://masreplay.s3.amazonaws.com/fa3a06cf-6e00-41bb-a113-9c3ac47b89a4",
        )

        # don't forget to set cache_time=1 for testing (default is 300s or 5m)
        await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()

    types.ReplyKeyboardRemove()

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('تم الالغاء', reply_markup=types.ReplyKeyboardRemove())


async def on_startup(_):
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(settings().WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(_):
    logging.warning('Bye! Shutting down webhook connection')


def main():
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=settings().WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=settings().WEBAPP_HOST,
        port=settings().WEBAPP_PORT,
    )


if __name__ == '__main__':
    from aiogram.utils import executor

    executor.start_polling(dp, skip_updates=True)
