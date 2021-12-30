from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
from core.config import get_settings

settings = get_settings()


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.teacher.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.teacher.create(db, obj_in=user_in)  # noqa: F841
