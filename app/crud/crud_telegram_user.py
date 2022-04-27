from app import schemas
from app.crud.base import CRUDBase
from app.models import TelegramUser
from app.schemas.telegram_user import TelegramUserCreate, TelegramUserUpdate


class CRUDTelegramUser(CRUDBase[TelegramUser, TelegramUserCreate, TelegramUserUpdate, schemas.TelegramUser]):
    @staticmethod
    def is_blocked(user: schemas.TelegramUser):
        return user.is_blocked


telegram_user = CRUDTelegramUser(TelegramUser, schemas.TelegramUser)
