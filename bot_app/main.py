# https://github.com/aiogram/aiogram/blob/dev-2.x/examples/callback_data_factory.py
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from bot_app import middlewares

from app.core.config import settings

logging.basicConfig(level=logging.INFO)

API_TOKEN = settings().TELEGRAM_BOT_API_TOKEN
bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
middlewares.setup(dispatcher=dp)

from bot_app.handlers import *


async def on_startup(_):
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(settings().WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(_):
    logging.warning('Bye! Shutting down webhook connection')


def main():
    executor.start_polling(
        dp,
        skip_updates=True,
    )


if __name__ == '__main__':
    main()
