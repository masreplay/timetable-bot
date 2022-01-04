from sqlmodel import Session

import asc_scrapper.crud as asc_crud
from app import crud, schemas
from app.schemas.permission import new_user_permission
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
        role_in = schemas.Role(
            id=role.id,
            ar_name=role.ar_name,
            en_name=role.en_name,
            permission=new_user_permission.dict()
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


def init_db(db: Session):
    init_periods(db)
    init_roles(db)
    init_users(db)
