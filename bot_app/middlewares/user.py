from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app import schemas
from bot_app import service


class PermissionsMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        print(message.from_user)
        if not message.from_user.is_bot:
            user = schemas.TelegramUserCreate.parse_obj(dict(message.from_user))
            print(user)
            service.create_user(user)
            if message.from_user.id in []:
                await message.reply(text="Hello, me!", reply=False)


async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
    pass
