from aiogram import types
from aiogram.dispatcher.handler import SkipHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class PermissionsMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        print(message.from_user.id == 1)
        print(message.from_user)
        if message.from_user.id in []:
            await message.reply(text="Hello, me!", reply=False)


async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
    pass
