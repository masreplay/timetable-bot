from sqlmodel import select, Session

from app import schemas, models, crud
from app.schemas.enums import UserType
from app.schemas.schedule import ScheduleDetails, ScheduleDetailsItem
from bot_app.states import ScheduleType


class CRUDSchedule:
    # noinspection PyTypeChecker
    def default_stage_schedule(self, db: Session) -> ScheduleDetails:
        stage: schemas.Stage = next(iter(crud.stage.get_multi(db=db, skip=0, limit=1).results), None)
        return self.get_stage_schedule(db=db, stage=stage)

    def get_stage_schedule(
            self,
            db: Session,
            stage: schemas.Stage,
    ) -> ScheduleDetails:
        crud.stage.get(db=db,id=stage.id)
        return ScheduleDetails(
            item=ScheduleDetailsItem(
                id=stage.id,
                name=stage.name,
                type=ScheduleType.stages,
            ),
            cards=db.exec(
                select(models.Card).where(
                    models.Card.lesson.has(
                        models.Lesson.stages.any(models.Stage.id == stage.id),
                    )
                )
            ).all(),
            days=db.exec(select(models.Day)).all(),
            periods=db.exec(select(models.Period)).all(),
        )

    def get_teacher_schedule(
            self,
            db: Session,
            teacher: schemas.User,
    ) -> ScheduleDetails:
        return ScheduleDetails(
            item=ScheduleDetailsItem(
                id=teacher.id,
                name=teacher.name,
                type=ScheduleType.teachers,
            ),
            cards=db.query(models.Card).join(models.Lesson).join(models.User)
                .filter(models.User.id == teacher.id).all(),
            days=db.exec(select(models.Day)).all(),
            periods=db.exec(select(models.Period)).all(),
        )

    def get_classroom_schedule(
            self,
            db: Session,
            classroom: schemas.Room,
    ) -> ScheduleDetails:
        return ScheduleDetails(
            item=ScheduleDetailsItem(
                id=classroom.id,
                name=classroom.name,
                type=ScheduleType.teachers,
            ),
            cards=db.query(models.Card).join(models.Lesson).join(models.Room)
                .filter(models.Room.id == classroom.id).all(),
            days=db.exec(select(models.Day)).all(),
            periods=db.exec(select(models.Period)).all(),
        )

    def get_subject_schedule(
            self,
            db: Session,
            subject: schemas.Subject,
    ) -> ScheduleDetails:
        return ScheduleDetails(
            item=ScheduleDetailsItem(
                id=subject.id,
                name=subject.name,
                type=ScheduleType.teachers,
            ),
            cards=db.query(models.Card).join(models.Lesson).join(models.Subject)
                .filter(models.Subject.id == subject.id).all(),
            days=db.exec(select(models.Day)).all(),
            periods=db.exec(select(models.Period)).all(),
        )

    def get_multi(self, db: Session) -> schemas.Schedule:
        return schemas.Schedule(
            days=db.exec(select(models.Day)).all(),
            periods=db.exec(select(models.Period)).all(),
            cards=db.exec(select(models.Card)).all(),
            lessons=db.exec(select(models.Lesson)).all(),
            buildings=db.query(models.Building).all(),
            floors=db.exec(select(models.Floor)).all(),
            classrooms=db.exec(select(models.Stage)).all(),
            subjects=db.exec(select(models.Subject)).all(),
            teachers=db.exec(
                select(models.User).where(
                    models.User.job_titles.any(
                        models.JobTitle.type.in_([UserType.teacher])
                    )
                )
            ).all(),
            stages=db.exec(select(models.Stage)).all(),
        )
