from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from public.patron.models import Patron, PatronCreate, PatronUpdate

from typing import Sequence


def create_patron(patron: PatronCreate, db: Session = Depends(get_session)) -> Patron:
    patron = Patron.model_validate(patron)
    db.add(patron)
    db.commit()
    db.refresh(patron)
    return patron


def read_patrons(
    offset: int = 0, limit: int = 20, db: Session = Depends(get_session)
) -> Sequence[Patron]:
    patrons = db.exec(select(Patron).offset(offset).limit(limit)).all()
    return patrons


def read_patron(patron_id: int, db: Session = Depends(get_session)) -> Patron:
    patron = db.get(Patron, patron_id)
    if not patron:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patron not found with id: {patron_id}",
        )
    return patron


def update_patron(
    patron_id: int, patron: PatronUpdate, db: Session = Depends(get_session)
) -> Patron:
    patron_to_update = db.get(Patron, patron_id)
    if not patron_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patron not found with id: {patron_id}",
        )

    patch = patron.model_dump(exclude_unset=True)
    for key, value in patch.items():
        setattr(patron_to_update, key, value)

    db.add(patron_to_update)
    db.commit()
    db.refresh(patron_to_update)
    return patron_to_update


def delete_patron(patron_id: int, db: Session = Depends(get_session)) -> dict:
    patron = db.get(Patron, patron_id)
    if not patron:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patron not found with id: {patron_id}",
        )

    db.delete(patron)
    db.commit()
    return {"ok": True}
