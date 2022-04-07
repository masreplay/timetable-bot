from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app import schemas, crud
from app.core.image import aws
from app.db.db import get_db
from app.schemas import enums
from app.schemas.paging import Paging, paging, PagingParams

router = APIRouter()


@router.get("/", response_model=Paging[schemas.User])
def read_users(
        search_query: str | None = None,
        role_id: UUID | None = None,
        user_types: list[enums.StaffType] | None = None,
        job_titles: list[str] | None = Query(None),
        db: Session = Depends(get_db),
        p: PagingParams = Depends(paging),
) -> Any:
    """
    Retrieve users.
    """
    print(f"job_titlesjob_titlesjob_titles{job_titles}")
    users = crud.user.get_filter(db, skip=p.skip, limit=p.limit, query=search_query, role_id=role_id,
                                 user_types=user_types, job_titles=job_titles)
    return users


@router.get("/{id}", response_model=schemas.User)
def read_user(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get user by ID.
    """
    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=schemas.User)
async def create_user(
        *,
        image: UploadFile | None = File(None),
        user_in: schemas.UserCreate = Depends(schemas.UserCreate.as_form),
        db: Session = Depends(get_db),
) -> Any:
    """
    Create new user.
    """

    user = crud.user.get_by_name(db=db, name=user_in.name)
    if user:
        raise HTTPException(status_code=400, detail="User already exist")

    if not crud.role.get(db=db, id=user_in.role_id):
        raise HTTPException(status_code=404, detail="Role not found")

    try:
        user = crud.user.create_relation(
            db=db,
            obj_in=user_in,
            image_url=aws.upload_image(image)
        )
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Job titles are duplicated or not exits")


@router.put("/{id}", response_model=schemas.User)
def update_user(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        image: UploadFile | None = File(None),
        user_in: schemas.UserUpdate = Depends(schemas.UserUpdate.as_form),
        job_titles: list[str] = Form([])
) -> Any:
    """
    Update a user.
    """

    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    role = crud.role.get(db=db, id=user_in.role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    try:
        user = crud.user.update(
            db=db,
            db_obj=user,
            obj_in=dict(**user_in.dict(), image_url=aws.upload_image(image)),
            job_titles=job_titles
        )
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Job titles are duplicated or not exits")


@router.delete("/{id}", response_model=schemas.Message)
def delete_user(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a user.
    """
    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.user.remove(db=db, id=id)
    return schemas.Message(detail="User deleted")
