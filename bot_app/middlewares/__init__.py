from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot_app.middlewares.user import UserMiddleware


def setup(dispatcher: Dispatcher):
    dispatcher.middleware.setup(LoggingMiddleware("bot"))
    dispatcher.middleware.setup(UserMiddleware())
    dispatcher.middleware.setup(LoggingMiddleware())
