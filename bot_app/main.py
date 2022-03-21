import logging
import uuid
from enum import Enum

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, \
    InlineQueryResultPhoto
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

from app import schemas
from app.core.config import settings
from bot_app import service
from i18n import translate

logging.basicConfig(level=logging.INFO)

API_TOKEN = settings().TELEGRAM_BOT_API_TOKEN

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


# States
class StageScheduleForm(StatesGroup):
    branch = State()
    stage = State()


class Form(StatesGroup):
    teachers = State()
    classrooms = State()
    classes = State()
    lessons = State()


class Commands(str, Enum):
    start = "start"
    schedule = "schedule"
    cancel = "cancel"
    test = "test"


# https://github.com/aiogram/aiogram/blob/dev-2.x/examples/callback_data_factory.py
classrooms_cb = CallbackData('select', 'id', 'action')  # classrooms:<id>:<action>


@dp.message_handler(commands=Commands.start)
async def cmd_schedule(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    markup.add("مرحلة دراسية 🏬")
    markup.add("استاذ 🧑‍🏫")
    markup.add("مادة 📔")
    await StageScheduleForm.next()
    await message.reply("اختر نوع الجدول", reply_markup=markup)


@dp.message_handler(commands=Commands.schedule)
async def cmd_schedule(message: types.Message):
    """
    Get branch
    """

    await StageScheduleForm.branch.set()

    markup = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
    branches: list[schemas.Branch] = service.get_branches()

    markup.add(*[
        types.InlineKeyboardButton(text=branch.name,
                                   callback_data=classrooms_cb.new(id=str(branch.id), action='branch'))
        for branch in branches
    ])
    await message.reply(f"اختر الفرع", reply_markup=markup)


@dp.callback_query_handler(classrooms_cb.filter(action='branch'), state=StageScheduleForm.branch)
async def process_branch(query: types.CallbackQuery, callback_data: dict[str, str]):
    branch_id = callback_data['id']
    markup = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)

    stages: list[schemas.Stage] = service.get_stages(branch_id).results
    markup.add(*[
        types.InlineKeyboardButton(text=stage.name, callback_data=classrooms_cb.new(id=str(stage.id), action='stage'))
        for stage in stages
    ])

    await query.message.reply(f"اختر المرحلة", reply_markup=markup)

    await StageScheduleForm.next()


@dp.callback_query_handler(classrooms_cb.filter(action='stage'), state=StageScheduleForm.stage)
async def process_stage(query: types.CallbackQuery, callback_data: dict[str, str]):
    stage_id = callback_data['id']

    await query.message.reply('...جاري تحويل الصورة', reply_markup=types.ReplyKeyboardRemove())
    # Remove keyboard
    markup = types.InlineKeyboardMarkup()

    try:
        image_url = service.get_schedule_image_url(stage_id=stage_id)
        name = f'{image_url.name}'

        schedule_web_link = f"{settings().FRONTEND_URL}schedule/stages/{stage_id}"
        # And send message
        a = await bot.send_photo(
            chat_id=query.message.chat.id,
            caption=md.text(
                md.text(f"جدول: {md.link(name, schedule_web_link)}"),
                sep='\n',
            ),
            photo=image_url.url,
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
        await bot.pin_chat_message(chat_id=query.message.chat.id, message_id=a.message_id)
    except Exception as e:
        await bot.send_message(chat_id=query.message.chat.id, text="حدث خطأ")


@dp.message_handler(commands='teachers')
async def cmd_schedule(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    await message.reply("استاذة القسم؟", reply_markup=markup)


@dp.message_handler(commands='about')
async def cmd_about(message: types.Message):
    buttons = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)

    buttons.add(types.InlineKeyboardButton('منو سوة هذا البرنامج؟', callback_data='credits'))
    buttons.add(types.InlineKeyboardButton('شنو الطريقة السوينا بيها؟', callback_data='technologies'))
    buttons.add(types.InlineKeyboardButton('شلون يشتغل؟', callback_data='how_does_it_work'))

    await bot.send_message(
        chat_id=message.chat.id,
        text=md.text(translate("ar", "about")),
        reply_markup=buttons,
        parse_mode=ParseMode.MARKDOWN,
    )


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
    executor.start_polling(
        dp,
        skip_updates=True,
    )


if __name__ == '__main__':
    main()
