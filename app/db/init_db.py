import re
from uuid import UUID, uuid4

from sqlmodel import Session

import asc_scrapper.schemas as asc_schemas
from app import crud, schemas, models
from app.core.config import settings
from app.schemas import enums
from app.schemas.enums import UserType, CollageShifts
from app.schemas.permissions import default_permissions
from asc_scrapper.crud import AscCRUD
from uot_scraper.match_teachers import get_combine_teachers, MergedTeacher


class InitializeDatabaseWithASC:
    db: Session
    asc: AscCRUD

    building_ids: dict[str, UUID] = {}
    rooms_ids: dict[str, UUID] = {}
    periods_ids: dict[str, UUID] = {}
    lessons_ids: dict[str, UUID] = {}
    subjects_ids: dict[str, UUID] = {}
    stages_ids: dict[str, UUID] = {}
    teachers_ids: dict[str, UUID] = {}
    cards_ids: dict[str, UUID] = {}
    days_ids: dict[str, UUID] = {}

    def __init__(self, db: Session, asc_crud: AscCRUD):
        self.db = db
        self.asc = asc_crud

    def init_building(self):
        buildings = self.asc.get_all(asc_schemas.Building)

        for building in buildings:
            self.building_ids[building.id] = crud.building.create(
                db=self.db,
                obj_in=schemas.BuildingCreate(
                    name=building.name,
                    color=building.color,
                )
            ).id

    def init_subjects(self):
        subjects = self.asc.get_all(asc_schemas.Subject)
        for subject in subjects:
            self.subjects_ids[subject.id] = crud.subject.create(
                db=self.db,
                obj_in=schemas.SubjectCreate(
                    name=subject.name,
                    color=subject.color,
                )
            ).id

    def init_classes(self):
        computer_science_department = crud.department.create(
            db=self.db, obj_in=schemas.DepartmentCreate(
                name="علوم الحاسوب",
                en_name="Computer Science",
                abbr="CS",
                vision=None,
            )
        )
        branches = [
            schemas.Branch(
                id=uuid4(),
                name="برمجيات",
                en_name="Software",
                abbr="SW",
                vision=None,
                department_id=computer_science_department.id
            ),
            schemas.Branch(
                id=uuid4(),
                name="نظم",
                en_name="Information Systems",
                abbr="IS",
                vision=None,
                department_id=computer_science_department.id
            ),
            schemas.Branch(
                id=uuid4(),
                name="ذكاء",
                en_name="Artificial Intelligence",
                abbr="AI",
                vision=None,
                department_id=computer_science_department.id
            ),
            schemas.Branch(
                id=uuid4(),
                name="امنية",
                en_name="Computer Security",
                abbr="CS",
                vision=None,
                department_id=computer_science_department.id
            ),
            schemas.Branch(
                id=uuid4(),
                name="شبكات",
                en_name="Networks",
                abbr="NW",
                vision=None,
                department_id=computer_science_department.id
            ),
            schemas.Branch(
                id=uuid4(),
                name="وسائط",
                en_name="Multimedia",
                abbr="MM",
                vision=None,
                department_id=computer_science_department.id
            ),
        ]
        for branch in branches:
            crud.branch.create(
                db=self.db, obj_in=branch
            )

        other = crud.branch.create(
            db=self.db, obj_in=schemas.BranchCreate(
                id=uuid4(),
                name="اخرى",
                en_name="",
                abbr="MM",
                vision=None,
                department_id=computer_science_department.id
            ),
        )

        levels: dict[str, int] = {
            "أول": 1,
            "ثاني": 2,
            "ثالث": 3,
            "رابع": 4,
        }
        shifts: dict[str, CollageShifts] = {
            "صباحي": CollageShifts.morning,
            "مسائي": CollageShifts.evening,
        }
        classes = self.asc.get_all(asc_schemas.Class)

        for class_ in classes:
            if class_.name not in ["", " "]:
                if len(class_.name.split()) < 3:
                    self.stages_ids[class_.id] = crud.stage.create(
                        db=self.db, obj_in=schemas.StageCreate(
                            name=class_.name,
                            shift=CollageShifts.morning,
                            level=None,
                            branch_id=other.id,
                        )
                    ).id
                else:
                    name = re.sub(' +', ' ', class_.name)

                    level, branch, branch2, shift = name.split()
                    level = levels[level]
                    shift = shifts[shift]
                    branch: schemas.Branch = list(filter(lambda b: b.name == branch, branches))[0]

                    self.stages_ids[class_.id] = crud.stage.create(
                        db=self.db, obj_in=schemas.StageCreate(
                            shift=shift,
                            level=level,
                            branch_id=branch.id,
                        )
                    ).id

    def init_lessons(self):
        lessons = self.asc.get_all(asc_schemas.Lesson)
        for lesson in lessons:
            print(f"self.rooms_ids {self.rooms_ids[lesson.classroom_id] if lesson.classroom_id else None}")
            lesson_id = crud.lesson.create(
                db=self.db,
                obj_in=schemas.LessonCreate(
                    room_id=self.rooms_ids[lesson.classroom_id] if lesson.classroom_id else None,
                    subject_id=self.subjects_ids[lesson.subjectid],
                    teacher_id=self.teachers_ids[lesson.teacherids[0]] if lesson.teacherids else None,
                )
            ).id
            self.lessons_ids[lesson.id] = lesson_id
            for stage_id in lesson.classids:
                self.db.add(models.StageLesson(stage_id=self.stages_ids.get(stage_id), lesson_id=lesson_id))

    def init_rooms(self):
        rooms = self.asc.get_all(asc_schemas.Classroom)
        for room in rooms:
            self.rooms_ids[room.id] = crud.room.create(
                db=self.db,
                obj_in=schemas.RoomCreate(
                    name=room.name,
                    color=room.color,
                    building_id=self.building_ids.get(room.buildingid),
                    type=enums.RoomType.classroom
                )
            ).id

    def init_periods(self):
        periods = self.asc.get_all(asc_schemas.Period)
        for period in periods:
            self.periods_ids[period.id] = crud.period.create(db=self.db, obj_in=schemas.PeriodCreate(
                start_time=period.starttime,
                end_time=period.endtime,
            )).id

    def init_days(self):
        days: list[asc_schemas.Day] = self.asc.get_all(asc_schemas.Day)
        for day in days:
            if day.name not in ["Any day", "Every day"]:
                self.days_ids[day.vals[0]] = crud.day.create(
                    db=self.db,
                    obj_in=schemas.DayCreate(
                        name=day.name
                    )
                ).id

    def init_cards(self):
        cards: list[asc_schemas.Card] = self.asc.get_all(asc_schemas.Card)
        for card in cards:
            self.cards_ids[card.id] = crud.card.create(
                db=self.db,
                obj_in=schemas.CardCreate(
                    period_id=self.periods_ids[card.period],
                    day_id=self.days_ids[card.days],
                    lesson_id=self.lessons_ids[card.lessonid],
                )
            ).id

    def init_db(self) -> bool:
        user = crud.user.get_by_email(self.db, email="pts@gmail.com")
        if not user:
            self.init_building()
            self.init_classes()
            self.init_subjects()
            self.init_rooms()
            self.init_periods()
            self.init_days()

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
                crud.job_title.create(self.db, obj_in=job_title)

            # crud.user.update_job_titles_by_email(self.db, email=user.email, job_titles=[creator_jt])

            default_role = crud.role.create(
                db=self.db, obj_in=schemas.RoleCreate(
                    ar_name="مستخدم جديد",
                    en_name="default",
                    permissions=default_permissions,
                )
            )
            user: schemas.User = crud.user.create(
                db=self.db, obj_in=schemas.UserCreateDB(
                    email="pts@gmail.com",
                    password="password",
                    color='#000000',
                    gender=None,
                    name="بطس",
                    en_name="pts",
                    role_id=default_role.id
                )
            )
            crud.user.update_job_titles(self.db, id=user.id, job_titles=[student_jt, creator_jt])

            teachers: list[MergedTeacher] = get_combine_teachers(self.asc)
            for teacher in teachers:
                user = crud.user.create(db=self.db, obj_in=schemas.UserCreateDB(
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
                crud.user.update_job_titles(self.db, id=user.id, job_titles=[teacher_jt])
                self.teachers_ids[teacher.id] = user.id

            # Update Mr. osama job titles
            for teacher_email in settings().RESPONSIBLE_USERS:
                user: schemas.User = crud.user.get_by_email(self.db, email=teacher_email)
                if user:
                    crud.user.update_job_titles(self.db, id=user.id, job_titles=[teacher_jt, responsible_jt])

            self.init_lessons()
            self.init_cards()
            return True
        else:
            return False
