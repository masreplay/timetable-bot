from sqlmodel import Session, select

from app import schemas
from app.crud.base import CRUDBase
from app.models import Subject
from app.schemas import Paging
from app.schemas.subject import SubjectCreate, SubjectUpdate


class CRUDSubject(CRUDBase[Subject, SubjectCreate, SubjectUpdate, schemas.Subject]):

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> Paging[schemas.Subject]:
        return Paging[schemas.Subject](
            count=db.query(Subject).count(),
            results=db.exec(select(Subject).order_by(Subject.name).offset(skip).limit(limit)).all()
        )


subject: CRUDSubject = CRUDSubject(Subject, schemas.Subject)
