from uuid import UUID

from sqlmodel import Session, select

from app import crud, schemas
from app.schemas import Role
from core.config import get_settings

# Seed data base
from uot_scraper.db import get_roles
from uot_scraper.match_teachers import get_acs_uot_teachers

settings = get_settings()


def init_db(db: Session) -> None:
    users = crud.user.get_multi(db=db, limit=1000)
    for teacher in users:
        db.delete(teacher)

    roles = crud.role.get_multi(db=db, limit=1000)
    for role in roles:
        db.delete(role)

    db.commit()
    roles = get_roles()
    for role in roles:
        role_in = schemas.Role(
            id=role.id,
            ar_name=role.ar_name,
            en_name=role.en_name
        )
        db.add(role_in)
        db.commit()

    teachers = get_acs_uot_teachers()
    for teacher in teachers:
        crud.user.create(db, obj_in=teacher)
