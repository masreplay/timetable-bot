import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from app import schemas
from app.core.config import settings
from app.schemas.image_url import ImageUrl
from bot_app import service
from bot_app.handlers.callbackes import classrooms_cb
from bot_app.main import dp, bot
from bot_app.states import ScheduleType, StageScheduleForm
from bot_app.status import MESSAGE_500_INTERNAL_SERVER_ERROR


@dp.callback_query_handler(lambda c: c.data == ScheduleType.teachers)
async def process_teacher_schedule(query: types.CallbackQuery):
    await StageScheduleForm.branch.set()

    markup = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
    teachers = service.get_teachers()

    markup.add(*[
        types.InlineKeyboardButton(text=teacher.name, callback_data=str(teacher.id))
        for teacher in teachers
    ])
    await query.message.reply(f"اختر الاستاذ", reply_markup=markup)
