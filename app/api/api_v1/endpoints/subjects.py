from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.Subject])
def read_subjects(
        db: Session = Depends(get_db),
        paging: LimitSkipParams = Depends(),
) -> Any:
    """
    Retrieve subjects.
    """
    subjects = crud.subject.get_multi(db, skip=paging.skip, limit=paging.limit)
    return subjects


@router.post("/", response_model=schemas.Subject)
def create_subject(
        *,
        db: Session = Depends(get_db),
        subject_in: schemas.SubjectCreate,
) -> Any:
    """
    Create new subject.
    """
    subject = crud.subject.create(db=db, obj_in=subject_in)
    return subject


@router.put("/{id}", response_model=schemas.Subject)
def update_subject(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        subject_in: schemas.SubjectUpdate,
) -> Any:
    """
    Update a subject.
    """
    subject = crud.subject.get(db=db, id=id)
    if not subject:
        raise HTTPException(status_code=404, detail="subject not found")
    subject = crud.subject.update(db=db, db_obj=subject, obj_in=subject_in)
    return subject


@router.get("/{id}", response_model=schemas.Subject)
def read_subject(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get subject by ID.
    """
    subject = crud.subject.get(db=db, id=id)
    if not subject:
        raise HTTPException(status_code=404, detail="subject not found")
    return subject


@router.delete("/{id}", response_model=schemas.Subject)
def delete_subject(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a subject.
    """
    subject = crud.subject.get(db=db, id=id)
    if not subject:
        raise HTTPException(status_code=404, detail="subject not found")
    subject = crud.subject.remove(db=db, id=id)
    return subject
