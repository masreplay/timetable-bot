from uuid import UUID

from sqlmodel import Session, select

from app import crud, schemas
from app.schemas import Role
from core.config import get_settings

# Seed data base
from uot_scraper.db import get_teachers, get_roles

settings = get_settings()


def init_db(db: Session) -> None:
    teachers = crud.teacher.get_multi(db=db, limit=1000)
    for teacher in teachers:
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

    teachers = get_teachers()
    for teacher in teachers:
        teacher_in = schemas.TeacherCreate(
            en_name=teacher.en_name,
            ar_name=teacher.ar_name,
            role_id=UUID(teacher.role_id),
        )
        crud.teacher.create(db, obj_in=teacher_in)
