from sqlmodel import Session, select

from app import schemas
from app.crud.base import CRUDBase
from app.models import Stage
from app.schemas.stage import StageCreate, StageUpdate


class CRUDStage(CRUDBase[Stage, StageCreate, StageUpdate, Stage]):

    def get_by_object(self, db: Session, stage: StageCreate | StageUpdate) -> Stage:
        statement = select(Stage) \
            .where(*[Stage.branch_id == stage.branch_id, Stage.shift == stage.shift, Stage.level == stage.level])
        return db.exec(statement).first()


stage: CRUDStage = CRUDStage(Stage, schemas.Stage)
