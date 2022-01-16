from sqlmodel import Session, select

from sqlmodel import Session, select

from app import schemas
from app.crud.base import CRUDBase
from app.models import Branch
from app.schemas import Paging
from app.schemas.branch import BranchCreate, BranchUpdate


class CRUDBranch(CRUDBase[Branch, BranchCreate, BranchUpdate, schemas.Branch]):

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> Paging[schemas.Branch]:
        return Paging[schemas.Branch](
            count=db.query(Branch).count(),
            results=db.exec(select(Branch).order_by(Branch.name).offset(skip).limit(limit)).all()
        )


branch: CRUDBranch = CRUDBranch(Branch, schemas.Branch)
