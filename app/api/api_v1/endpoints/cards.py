from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, crud
from app.db.db import get_db
from app.schemas.paging import *

router = APIRouter()


@router.get("/", response_model=Paging[schemas.Card])
def read_cards(
        db: Session = Depends(get_db),
        paging: LimitSkipParams = Depends(),
) -> Any:
    """
    Retrieve cards.
    """
    cards = crud.card.get_multi(db, skip=paging.skip, limit=paging.limit)
    return cards


@router.post("/", response_model=schemas.Card)
def create_card(
        *,
        db: Session = Depends(get_db),
        card_in: schemas.CardCreate,
) -> Any:
    """
    Create new card.
    """
    card = crud.card.create(db=db, obj_in=card_in)
    return card


@router.put("/{id}", response_model=schemas.Card)
def update_card(
        *,
        db: Session = Depends(get_db),
        id: UUID,
        card_in: schemas.CardUpdate,
) -> Any:
    """
    Update a card.
    """
    card = crud.card.get(db=db, id=id)
    if not card:
        raise HTTPException(status_code=404, detail="card not found")
    card = crud.card.update(db=db, db_obj=card, obj_in=card_in)
    return card


@router.get("/{id}", response_model=schemas.Card)
def read_card(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Get card by ID.
    """
    card = crud.card.get(db=db, id=id)
    if not card:
        raise HTTPException(status_code=404, detail="card not found")
    return card


@router.delete("/{id}", response_model=schemas.Card)
def delete_card(
        *,
        db: Session = Depends(get_db),
        id: UUID,
) -> Any:
    """
    Delete a card.
    """
    card = crud.card.get(db=db, id=id)
    if not card:
        raise HTTPException(status_code=404, detail="card not found")
    card = crud.card.remove(db=db, id=id)
    return card
