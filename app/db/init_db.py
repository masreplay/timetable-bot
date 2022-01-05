from sqlmodel import Session

import asc_scrapper.crud as asc_crud
from app import crud, schemas
from app.core.config import settings
from app.schemas.permissions import default_permissions, Permissions
from uot_scraper.db import get_roles
from uot_scraper.match_teachers import get_acs_uot_teachers


def init_users(db: Session):
    users = crud.user.get_multi(db=db, limit=1000).results
    for user in users:
        crud.user.remove(db=db, id=user.id)

    teachers = get_acs_uot_teachers()
    for user in teachers:
        crud.user.create(db, obj_in=user)


def init_roles(db: Session):
    roles = crud.role.get_multi(db=db, limit=1000).results
    for role in roles:
        crud.role.remove(db=db, id=role.id)

    roles = get_roles()
    for role in roles:
        role_in = schemas.RoleSchema(
            id=role.id,
            ar_name=role.ar_name,
            en_name=role.en_name,
            permissions=default_permissions
        )
        db.add(role_in)
        db.commit()


def init_periods(db: Session):
    periods = crud.period.get_multi(db=db, limit=1000).results
    for period in periods:
        crud.period.remove(db=db, id=period.id)

    periods = asc_crud.get_periods()
    for period in periods:
        period = schemas.Period(
            start_time=period.starttime,
            end_time=period.endtime,
        )
        db.add(period)
        db.commit()


def init_super_admin(db: Session):
    user = crud.user.get_by_email(db, email=settings().FIRST_SUPERUSER)
    if not user:
        full_crud_permission = schemas.PermissionGroup(
            create=True,
            read=True,
            update=True,
            delete=True,
        )
        role: schemas.RoleSchema = crud.role.create(
            db, obj_in=schemas.RoleCreate(
                ar_name="مسؤول",
                en_name="SUPER ADMIN",
                permissions=Permissions(
                    users=full_crud_permission,
                    roles=full_crud_permission,
                    periods=full_crud_permission,
                ),
            )
        )
        crud.user.create(
            db, obj_in=schemas.UserCreate(
                email=settings().FIRST_SUPERUSER,
                password=settings().FIRST_SUPERUSER_PASSWORD,
                color='#000000',
                gender=None,
                en_name="SUPER ADMIN",
                name="مسؤول",
                role_id=role.id
            )
        )
        role: schemas.RoleSchema = crud.role.create(
            db, obj_in=schemas.RoleCreate(
                ar_name="تبطيس",
                en_name="PTS",
                permissions=default_permissions,
            )
        )
        crud.user.create(
            db, obj_in=schemas.UserCreate(
                email="pts@gmail.com",
                password="password",
                color='#000000',
                gender=None,
                name="بطس",
                en_name="pts",
                role_id=role.id
            )
        )


def init_db(db: Session):
    user = crud.user.get_by_email(db, email=settings().FIRST_SUPERUSER)
    if not user:
        init_periods(db)
        init_roles(db)
        init_users(db)
        init_super_admin(db)
