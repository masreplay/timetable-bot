from sqlalchemy.orm import load_only, joinedload
from sqlmodel import select, Session

from app import schemas, models
from app.schemas.enums import UserType


class CRUDSchedule:
    def get(self, db: Session) -> schemas.Schedule:
        return schemas.Schedule(
            days=db.exec(select(models.Day)).all(),
            periods=db.exec(select(models.Period)).all(),

            cards=db.exec(select(models.Card)).all(),
            lessons=db.exec(select(models.Lesson)).all(),

            buildings=db.exec(select(models.Building)).all(),
            floors=db.exec(select(models.Floor)).all(),
            classrooms=db.exec(select(models.Stage)).all(),

            subjects=db.exec(select(models.Subject)).all(),

            teachers=db.exec(select(models.User).where(
                models.User.job_titles.any(models.JobTitle.type.in_([UserType.teacher])))).all(),
            stages=db.exec(select(models.Stage)).all(),
        )
