from uuid import UUID

from pydantic import Field

from app.schemas.telegram import TelegramUser as TelegramUserSchema


class TelegramUserBase(TelegramUserSchema):
    is_blocked: bool = Field(False)


class TelegramUser(TelegramUserBase):
    id: UUID
    # TODO: migrate
    nickname: str | None


# Properties to receive via API on creation
class TelegramUserCreate(TelegramUserBase):
    pass


# Properties to receive via API on update
class TelegramUserUpdate(TelegramUserBase):
    pass
