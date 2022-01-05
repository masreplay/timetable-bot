from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel, select, Session
from sqlmodel import and_

from app.schemas.paging import Paging

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


@dataclass
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: Type[ModelType]

    def get(self, db: Session, id: UUID) -> Optional[ModelType]:
        statement = select(self.model).where(self.model.id == id)
        return db.exec(statement).first()

    def get_multi(
            self, db: Session, *, skip: UUID = 0, limit: UUID = 100
    ) -> Paging[ModelType]:
        where = []
        statement = select(self.model).where(*where).offset(skip).limit(limit)
        return Paging[ModelType](
            count=db.query(self.model).filter(*where).count(),
            results=db.exec(statement).all()
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID) -> ModelType:
        obj = self.get(db, id)
        db.delete(obj)
        db.commit()
        return obj
