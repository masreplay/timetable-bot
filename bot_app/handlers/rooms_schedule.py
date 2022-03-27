import math
from uuid import UUID

import aiogram.utils.markdown as md
from aiogram import types
from aiogram.types import ParseMode

from app.core.config import settings
from app.schemas.image_url import ImageUrl
from bot_app import service
from bot_app.handlers.callbackes import rooms_paging_cb, room_cb
from bot_app.main import dp, bot
from bot_app.service import default_per_page
from bot_app.status import MESSAGE_500_INTERNAL_SERVER_ERROR
from bot_app.utils.paging import get_paging_buttons


@dp.callback_query_handler(rooms_paging_cb.filter(action='paging'))
async def paging_rooms_cb_handler(query: types.CallbackQuery, callback_data: dict[str, str]):
    page: int = int(callback_data["page"])

    markup = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
    rooms_paging = service.get_rooms(page=page, per_page=default_per_page)

    markup.add(*[
        types.InlineKeyboardButton(text=room.name, callback_data=room_cb.new(id=str(room.id), action="select"))
        for room in rooms_paging.results
    ])

    markup.add(*get_paging_buttons(page, rooms_paging.count, rooms_paging_cb))

    pages_count = math.ceil(rooms_paging.count / default_per_page)
    await bot.edit_message_text(
        f'صفحة {page} من {pages_count}',
        query.from_user.id,
        query.message.message_id,
        reply_markup=markup,
    )


@dp.callback_query_handler(room_cb.filter(action='select'))
async def select_room_cb_handler(query: types.CallbackQuery, callback_data: dict[str, str]):
    room_id = UUID(callback_data["id"])

    await query.message.reply('جاري ارسال الجدول...', reply_markup=types.ReplyKeyboardRemove())

    markup = types.InlineKeyboardMarkup()

    response = service.get_schedule_image_url(classroom_id=room_id)

    if response.status_code == 200:
        image_url = ImageUrl.parse_obj(response.json())

        schedule_front_url = f"{settings().FRONTEND_URL}/schedule/?room_id={room_id}"

        message = await bot.send_photo(
            chat_id=query.message.chat.id,
            caption=md.text(
                md.text(f"جدول: {md.link(image_url.name, schedule_front_url)}"),
                sep='\n',
            ),
            photo=image_url.url,
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
        await bot.pin_chat_message(chat_id=query.message.chat.id, message_id=message.message_id)

    else:
        await bot.send_message(chat_id=query.message.chat.id, text=MESSAGE_500_INTERNAL_SERVER_ERROR)
