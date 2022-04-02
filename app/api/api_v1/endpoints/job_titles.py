from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.JobTitle])
def read_job_titles(
        db: Session = Depends(get_db),
        p: PagingParams = Depends(paging),
) -> Any:
    """
    Retrieve job_titles.
    """
    job_titles = crud.job_title.get_multi(db, skip=p.skip, limit=p.limit)
    return job_titles


@router.post("/", response_model=schemas.JobTitle)
def create_job_title(
        *,
        db: Session = Depends(get_db),
        job_title_in: schemas.JobTitleCreate,
) -> Any:
    """
    Create new job_title.
    """
    job_title = crud.job_title.create(db=db, obj_in=job_title_in)
    return job_title


@router.put("/{id}", response_model=schemas.JobTitle)
def update_job_title(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        job_title_in: schemas.JobTitleUpdate,
) -> Any:
    """
    Update a job_title.
    """
    job_title = crud.job_title.get(db=db, id=id)
    if not job_title:
        raise HTTPException(status_code=404, detail="Job title not found")
    job_title = crud.job_title.update(db=db, db_obj=job_title, obj_in=job_title_in)
    return job_title


@router.get("/{id}", response_model=schemas.JobTitle)
def read_job_title(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get job_title by ID.
    """
    job_title = crud.job_title.get(db=db, id=id)
    if not job_title:
        raise HTTPException(status_code=404, detail="Job title not found")
    return job_title


@router.delete("/{id}", response_model=schemas.Message)
def delete_job_title(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a job_title.
    """
    job_title = crud.job_title.get(db=db, id=id)
    if not job_title:
        raise HTTPException(status_code=404, detail="Job title not found")
    crud.job_title.remove(db=db, id=id)
    return schemas.Message(detail="Job title deleted")
