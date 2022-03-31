import json

from fastapi import File, UploadFile, Depends, HTTPException, APIRouter
from sqlmodel import Session

from app import schemas, crud
from app.api import deps
from app.api.deps import UserRole
from app.db.db import get_db
from app.db.init_db_v2 import InitializeDatabaseWithASCV2
from app.schemas import Message
from asc_scrapper.crud import AscCRUD

router = APIRouter()


@router.post("/")
async def seed_db(
        db: Session = Depends(get_db),
        upload_file: UploadFile = File(...),
        user_permissions: UserRole = Depends(deps.users_permission_handler),
):
    user, permissions = user_permissions
    json_data = json.load(upload_file.file)
    asc_init = InitializeDatabaseWithASCV2(
        db=db,
        asc_crud=AscCRUD(data=json_data)
    )
    asc_init.init_db()
    crud.asc_version.create(
        db=db,
        obj_in=schemas.AscVersionCreate(
            created_by=user.id,
            file_name=upload_file.filename,
        )
    )

    if asc_init:
        return Message(detail="Asc data has been init")
    else:
        raise HTTPException(400, detail="Data already exist")
