from uuid import UUID
from sqlmodel import Session, select
from app.crud.base import CRUDBase
from app.models import Stage
from app.schemas.stage import StageCreate, StageUpdate


class CRUDStage(CRUDBase[Stage, StageCreate, StageUpdate]):

    def get_object(self, db: Session, stage_: StageCreate) -> Stage:
        statement = select(self.model).where(Stage.fields.keys() == stage_.__fields__.keys())
        return db.exec(statement).first()


stage = CRUDStage(Stage)
