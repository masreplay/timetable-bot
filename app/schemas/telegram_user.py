from uuid import UUID

from app.schemas.telegram import TelegramUserBase


class TelegramUser(TelegramUserBase):
    id: UUID


# Properties to receive via API on creation
class TelegramUserCreate(TelegramUserBase):
    pass


# Properties to receive via API on update
class TelegramUserUpdate(TelegramUserBase):
    pass
