from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot_app.middlewares.user import PermissionsMiddleware


def setup(dispatcher: Dispatcher):
    dispatcher.middleware.setup(LoggingMiddleware("bot"))
    dispatcher.middleware.setup(PermissionsMiddleware())
    dispatcher.middleware.setup(LoggingMiddleware())
