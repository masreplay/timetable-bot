from dataclasses import dataclass
from typing import Any, Dict, Generic, Type, TypeVar
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel, select, Session

from app.schemas.paging import Paging

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)
Schema = TypeVar("Schema", bound=SQLModel)


@dataclass
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, Schema]):
    model: Type[ModelType]
    schema: Schema

    def get(self, db: Session, id: UUID) -> ModelType | None:
        statement = select(self.model).where(self.model.id == id)
        return db.exec(statement).first()

    def get_multi(
            self, db: Session, *, skip: UUID = 0, limit: UUID = 100
    ) -> Paging[Schema]:
        return Paging[self.schema](
            count=db.query(self.model).filter().count(),
            results=db.exec(select(self.model).offset(skip).limit(limit)).all()
        )

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: UpdateSchemaType | dict[str, Any]
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

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID) -> ModelType:
        obj = self.get(db, id)
        db.delete(obj)
        db.commit()
        return obj
