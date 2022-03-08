from datetime import datetime
from uuid import UUID

from sqlmodel import select, Session

from app import schemas, models, crud
from app.schemas import Paging
from app.schemas.enums import UserType
from app.schemas.rights import Rights
from app.schemas.schedule import ScheduleDetails
from app.schemas.schedule_information import get_schedule_information


class CRUDSchedule:
    # noinspection PyTypeChecker
    def get(self, db: Session, stage_id: UUID, teacher_id: UUID, stage: schemas.Stage | None) -> ScheduleDetails:
        return ScheduleDetails(
            stage=stage,
            information=get_schedule_information(
                validate_from=datetime.now().date(),
                validate_to=datetime.now().date(),
                collage_name="TODO",
                branch_name="TODO",
            ),
            rights=Rights(),
            cards=db.exec(
                select(models.Card).where(
                    models.Card.lesson.has(
                        models.Lesson.stages.any(models.Stage.id == stage_id),
                        # models.Lesson.teacher.id == teacher_id
                    )
                )
            ).all(),
            days=db.exec(select(models.Day)).all(),
            periods=db.exec(select(models.Period)).all(),
        )

    def default(self, db: Session, stage_id: UUID) -> ScheduleDetails:
        stages: list = crud.stage.get_multi(db=db, skip=0, limit=1).results
        stage: schemas.Stage = next(iter(stages), None)
        return self.get(db=db, stage_id=stage_id, stage=stage)

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
