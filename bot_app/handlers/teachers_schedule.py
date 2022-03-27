import math

from aiogram import types

from bot_app import service
from bot_app.handlers.callbackes import teachers_paging_cb, teacher_cb
from bot_app.main import dp, bot

default_per_page = 14


@dp.callback_query_handler(teachers_paging_cb.filter(action='paging'))
async def teachers_paging_cb_handler(query: types.CallbackQuery, callback_data: dict[str, str]):
    page: int = int(callback_data["page"])

    markup = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
    teachers_paging = service.get_teachers(page=page, per_page=default_per_page)

    markup.add(*[
        types.InlineKeyboardButton(text=teacher.name, callback_data=teacher_cb(id=str(teacher.id), action="select"))
        for teacher in teachers_paging.results
    ])

    paging_buttons = []

    if page != 1:
        paging_buttons.append(
            types.InlineKeyboardButton(
                text="⬅️",
                callback_data=teachers_paging_cb.new(page=page - 1, action='paging'),
            ),
        )

    if teachers_paging.count >= page * default_per_page:
        paging_buttons.append(
            types.InlineKeyboardButton(
                text="➡️",
                callback_data=teachers_paging_cb.new(page=page + 1, action='paging'),
            )
        )

    markup.row(*paging_buttons)
    pages_count = math.ceil(teachers_paging.count / default_per_page)
    await bot.edit_message_text(
        f'صفحة {page} من {pages_count}',
        query.from_user.id,
        query.message.message_id,
        reply_markup=markup,
    )


