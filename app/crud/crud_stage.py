from uuid import UUID

from sqlmodel import Session, select

from app import schemas, models
from app.crud.base import CRUDBase
from app.models import Stage, Branch
from app.schemas import Paging
from app.schemas.stage import StageCreate, StageUpdate


class CRUDStage(CRUDBase[Stage, StageCreate, StageUpdate, schemas.Stage]):

    def get_by_object(self, db: Session, stage: StageCreate | StageUpdate) -> Stage:
        statement = select(Stage) \
            .where(*[Stage.branch_id == stage.branch_id, Stage.shift == stage.shift, Stage.level == stage.level])
        return db.exec(statement).first()

    def get_filter(
            self, db: Session, *, skip: int = 0, limit: int = 100, branch_id: UUID | None, branch_name: str | None
    ) -> Paging[schemas.Stage]:
        where = []
        if branch_id:
            where.append(Stage.branch_id == branch_id)
        if branch_name:
            where.append(Stage.branch.has(Branch.name == branch_name))

        return Paging[schemas.Stage](
            count=db.query(Stage).filter(*where).count(),
            results=db.exec(select(Stage).where(*where).offset(skip).limit(limit)).all()
        )


stage: CRUDStage = CRUDStage(Stage, schemas.Stage)
