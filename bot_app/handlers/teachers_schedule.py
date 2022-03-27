from aiogram import types

from bot_app import service
from bot_app.handlers.callbackes import teachers_cb
from bot_app.main import dp, bot


def get_teachers_keyboard(page: int = 1):
    print(page)
    markup = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
    teachers = service.get_teachers(page=page, per_page=14).results

    markup.add(*[
        types.InlineKeyboardButton(text=teacher.name, callback_data=str(teacher.id))
        for teacher in teachers
    ])

    markup.row(
        types.InlineKeyboardButton(
            text=" ",
            callback_data=teachers_cb.new(page=page + 1, action='teacher'),
        ),
        types.InlineKeyboardButton(
            text="➡️",
            callback_data=teachers_cb.new(page=page - 1, action='teacher'),
        )
    )
    return markup


@dp.callback_query_handler(teachers_cb.filter(action='next'))
async def teachers_next_cb_handler(query: types.CallbackQuery, callback_data: dict[str, str]):
    page: int = int(callback_data["page"])

    await bot.edit_message_text(
        f'teacher',
        query.from_user.id,
        query.message.message_id,
        reply_markup=get_teachers_keyboard(page=page),
    )


@dp.callback_query_handler(teachers_cb.filter(action='previous'))
async def teachers_previous_cb_handler(query: types.CallbackQuery, callback_data: dict[str, str]):
    page: int = int(callback_data["page"])

    await bot.edit_message_text(
        f'teacher',
        query.from_user.id,
        query.message.message_id,
        reply_markup=get_teachers_keyboard(page=page),
    )
