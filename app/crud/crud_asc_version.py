from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select

from app import schemas
from app.models import AscVersion


class CRUDAscVersion:
    def create(self, db: Session, *, obj_in: schemas.AscVersionCreate) -> AscVersion:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = AscVersion(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(self, db: Session) -> list[AscVersion]:
        return db.exec(select(AscVersion)).all()
