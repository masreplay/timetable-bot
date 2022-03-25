import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot_app.commands import Commands
from bot_app.main import dp
from bot_app.states import ScheduleType


@dp.message_handler(commands=Commands.start)
async def cmd_start(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)

    schedule_type: dict[ScheduleType, str] = {
        ScheduleType.stages: "فرع",
        ScheduleType.teachers: "استاذ",
        ScheduleType.subjects: "مادة",
        ScheduleType.classrooms: "قاعة",
    }
    for callback, name in schedule_type.items():
        markup.add(types.InlineKeyboardButton(text=name, callback_data=callback))

    await message.reply("اختر نوع الجدول", reply_markup=markup)


# You can use state '*' if you need to handle all states.py
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals=['cancel', 'الغاء'], ignore_case=True), state='*')
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
