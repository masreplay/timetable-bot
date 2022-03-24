import logging
import uuid

import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, \
    InlineQueryResultPhoto
from aiogram.utils.callback_data import CallbackData

from app import schemas
from bot_app.commands import Commands
from bot_app.main import dp, bot
from bot_app.states import ScheduleTypeForm, ScheduleType
from i18n import translate

classrooms_cb = CallbackData('select', 'id', 'action')  # classrooms:<id>:<action>
schedule_type_cb = CallbackData('schedule', 'type')  # schedule:<type>


@dp.message_handler(commands=Commands.start)
async def cmd_start(message: types.Message):
    await ScheduleTypeForm.type.set()

    markup = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)

    schedule_type: dict[ScheduleType, str] = {
        ScheduleType.stages: "فرع",
        ScheduleType.teachers: "استاذ",
        ScheduleType.subjects: "مادة",
        ScheduleType.classrooms: "قاعة",
    }
    for key, value in schedule_type.items():
        markup.add(types.InlineKeyboardButton(text=value, callback_data=schedule_type_cb.new(type=key)))

    await message.reply("اختر نوع الجدول", reply_markup=markup)
    await ScheduleTypeForm.next()


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


@dp.callback_query_handler(lambda c: c.data == 'credits')
async def process_credits(call: types.CallbackQuery):
    await call.message.send_copy(
        chat_id=call.message.chat.id,
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


# You can use state '*' if you need to handle all states.py
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
