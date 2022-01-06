from sqlmodel import Session

import asc_scrapper.crud as asc_crud
from app import crud, schemas, models
from app.core.config import settings
from app.schemas.enums import UserType
from app.schemas.permissions import default_permissions, Permissions
from uot_scraper.db import get_roles
from uot_scraper.match_teachers import get_acs_uot_teachers


def init_roles(db: Session):
    roles = get_roles()
    for role in roles:
        role_in = models.Role(
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
        period = models.Period(
            start_time=period.starttime,
            end_time=period.endtime,
        )
        db.add(period)
        db.commit()


def init_db(db: Session):
    user = crud.user.get_by_email(db, email=settings().FIRST_SUPERUSER)
    if not user:
        init_roles(db)
        # define user title
        student_title = models.JobTitle(
            name="طالب",
            en_name="Student",
            type=UserType.student
        )
        representative_title = models.JobTitle(
            name="ممثل",
            en_name="Representative",
            type=UserType.student
        )

        teacher_title = models.JobTitle(
            name="مدرس",
            en_name="Teacher",
            type=UserType.teacher
        )
        responsible_title = models.JobTitle(
            name="المقرر",
            en_name="Responsible",
            type=UserType.teacher
        )
        assistant_teacher_title = models.JobTitle(
            name="مدرس مساعد",
            en_name="Assistant Teacher",
            type=UserType.teacher
        )

        employee_title = models.JobTitle(
            name="موظف",
            en_name="Employee",
            type=UserType.employee
        )

        creator_title = models.JobTitle(
            name="Constructor Team",
            en_name="Constructor Team",
            type=UserType.other
        )

        # Add job titles that will not add by relationship table
        for job_title in [employee_title, assistant_teacher_title, representative_title]:
            crud.job_title.create(db, obj_in=job_title)

        # teachers
        for teacher in get_acs_uot_teachers():
            db.add(models.User(
                job_titles=[teacher_title],
                name=teacher.name,
                en_name=teacher.en_name,
                image=teacher.image,
                email=teacher.email,
                uot_url=teacher.uot_url,
                role_id=teacher.role_id,
                hashed_password=None,
                color=teacher.color,
                asc_job=teacher.asc_job_title,
                asc_name=teacher.asc_name,
                scrape_from=teacher.scrape_from,
                gender=teacher.gender,
            ))
        db.commit()

        # Predefines users
        full_crud_permission = schemas.PermissionGroup(
            create=True,
            read=True,
            update=True,
            delete=True,
        )
        super_admin_role = crud.role.create(
            db, obj_in=schemas.RoleCreate(
                ar_name="مسؤول",
                en_name="SUPER ADMIN",
                permissions=Permissions(
                    users=full_crud_permission,
                    roles=full_crud_permission,
                    periods=full_crud_permission,
                    job_titles=full_crud_permission,
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
                role_id=super_admin_role.id,
                job_titles=[creator_title],
            )
        )
        default_role = crud.role.create(
            db, obj_in=schemas.RoleCreate(
                ar_name="مستخدم جديد",
                en_name="default",
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
                role_id=default_role.id,
                job_titles=[
                    student_title,
                    creator_title
                ]
            )
        )

        # Update Mr. osama job titles
        for teacher_email in settings().RESPONSIBLE_USERS:
            user = crud.user.get_by_email(db, email=teacher_email)
            if not user:
                continue
            for job in [teacher_title, responsible_title]:
                user.job_titles.append(job)
            db.add(user)
            db.commit()
