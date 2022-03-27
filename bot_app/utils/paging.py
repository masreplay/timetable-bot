from aiogram import types
from aiogram.utils.callback_data import CallbackData

from bot_app.service import default_per_page


def get_paging_buttons(page: int, count: int, callback: CallbackData) -> list[types.InlineKeyboardButton]:
    callback = CallbackData(callback.prefix, "page", "action")
    paging_buttons = []

    if count >= page * default_per_page:
        paging_buttons.append(
            types.InlineKeyboardButton(
                text="➡️",
                callback_data=callback.new(page=page + 1, action='paging'),
            )
        )
    if page != 1:
        paging_buttons.append(
            types.InlineKeyboardButton(
                text="⬅️",
                callback_data=callback.new(page=page - 1, action='paging'),
            ),
        )

    return paging_buttons
