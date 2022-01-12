import logging

from app import crud
from app import schemas
from app.core.config import settings
from app.db.db import get_db
# TODO: Call it inside do.py
from app.schemas.permissions import super_admin_permissions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with next(get_db()) as db:
        init_super_admin(db)


def init_super_admin(db):
    user = crud.user.get_by_email(db, email=settings().FIRST_SUPERUSER)
    if not user:
        super_admin_role = crud.role.create(
            db=db, obj_in=schemas.RoleCreate(
                ar_name="مسؤول",
                en_name="SUPER ADMIN",
                permissions=super_admin_permissions,
            )
        )
        crud.user.create(
            db=db, obj_in=schemas.UserCreate(
                email=settings().FIRST_SUPERUSER,
                password=settings().FIRST_SUPERUSER_PASSWORD,
                color='#000000',
                gender=None,
                en_name="SUPER ADMIN",
                name="مسؤول",
                role_id=super_admin_role.id,
            )
        )


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
