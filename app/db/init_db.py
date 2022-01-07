from sqlmodel import Session

import asc_scrapper.crud as asc_crud
from app import crud, schemas, models
from app.core.config import settings
from app.schemas.enums import UserType, CollageShifts
from app.schemas.permissions import default_permissions, Permissions
from uot_scraper.match_teachers import get_acs_uot_teachers


def init_classes(db: Session):
    computer_science_department = crud.department.create(
        db=db, obj_in=schemas.DepartmentCreate(
            name="علوم الحاسوب",
            en_name="Computer Science",
            abbr="CS",
            vision=None,
        )
    )
    software_branch = crud.branch.create(
        db=db, obj_in=schemas.BranchCreate(
            name="برمجيات",
            en_name="Software",
            abbr="SW",
            vision=None,
            department_id=computer_science_department.id
        )
    )
    stage = crud.stage.create(
        db=db, obj_in=schemas.StageCreate(
            shift=CollageShifts.morning,
            level=3,
            branch_id=software_branch.id,
        )
    )


def init_periods(db: Session):
    periods = asc_crud.get_periods()
    for period in periods:
        crud.period.create(db=db, obj_in=schemas.PeriodCreate(
            start_time=period.starttime,
            end_time=period.endtime,
        ))


def init_db(db: Session):
    user = crud.user.get_by_email(db, email=settings().FIRST_SUPERUSER)
    if not user:
        init_classes(db)
        # define user job titles
        student_jt = models.JobTitle(
            name="طالب",
            en_name="Student",
            type=UserType.student
        )
        representative_jt = models.JobTitle(
            name="ممثل",
            en_name="Representative",
            type=UserType.student
        )

        teacher_jt = models.JobTitle(
            name="مدرس",
            en_name="Teacher",
            type=UserType.teacher
        )
        responsible_jt = models.JobTitle(
            name="المقرر",
            en_name="Responsible",
            type=UserType.teacher
        )
        assistant_teacher_jt = models.JobTitle(
            name="مدرس مساعد",
            en_name="Assistant Teacher",
            type=UserType.teacher
        )

        employee_jt = models.JobTitle(
            name="موظف",
            en_name="Employee",
            type=UserType.employee
        )

        creator_jt = models.JobTitle(
            name="Constructor Team",
            en_name="Constructor Team",
            type=UserType.other
        )

        # Add job titles that will not add by relationship table
        for job_title in [employee_jt, assistant_teacher_jt, representative_jt]:
            crud.job_title.create(db, obj_in=job_title)

        # Predefines users
        full_crud_permission = schemas.PermissionGroup(
            create=True,
            read=True,
            update=True,
            delete=True,
        )
        super_admin_role = crud.role.create(
            db=db, obj_in=schemas.RoleCreate(
                ar_name="مسؤول",
                en_name="SUPER ADMIN",
                permissions=Permissions(
                    users=full_crud_permission,
                    roles=full_crud_permission,
                    periods=full_crud_permission,
                    job_titles=full_crud_permission,
                    departments=full_crud_permission,
                    branches=full_crud_permission,
                    stages=full_crud_permission,
                ),
            )
        )
        user = crud.user.create(
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
        crud.user.update_job_titles_by_email(db, email=user.email, job_titles=[creator_jt])

        default_role = crud.role.create(
            db=db, obj_in=schemas.RoleCreate(
                ar_name="مستخدم جديد",
                en_name="default",
                permissions=default_permissions,
            )
        )
        user = crud.user.create(
            db=db, obj_in=schemas.UserCreate(
                email="pts@gmail.com",
                password="password",
                color='#000000',
                gender=None,
                name="بطس",
                en_name="pts",
                role_id=default_role.id
            )
        )
        crud.user.update_job_titles_by_email(db, email=user.email, job_titles=[student_jt, creator_jt])

        # teachers
        for teacher in get_acs_uot_teachers():
            db.add(models.User(
                job_titles=[teacher_jt],
                name=teacher.name,
                en_name=teacher.en_name,
                image=teacher.image,
                email=teacher.email,
                uot_url=teacher.uot_url,
                role_id=default_role.id,
                color=teacher.color,
                asc_job=teacher.asc_job_title,
                asc_name=teacher.asc_name,
                scrape_from=teacher.scrape_from,
                gender=teacher.gender,
            ))
        db.commit()

        # Update Mr. osama job titles
        for teacher_email in settings().RESPONSIBLE_USERS:
            user = crud.user.get_by_email(db, email=teacher_email)
            if not user:
                continue
            crud.user.update_job_titles_by_email(db, email=user.email, job_titles=[teacher_jt, responsible_jt])
