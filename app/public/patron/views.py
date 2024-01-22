from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from database import get_session
from public.patron.crud import (
    create_patron,
    delete_patron,
    read_patron,
    read_patrons,
    update_patron,
)
from public.patron.models import PatronCreate, PatronRead, PatronUpdate

router = APIRouter()


@router.post("", response_model=PatronRead)
def create_a_patron(patron: PatronCreate, db: Session = Depends(get_session)):
    return create_patron(patron=patron, db=db)


@router.get("", response_model=list[PatronRead])
def get_patrons(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    return read_patrons(offset=offset, limit=limit, db=db)


@router.get("/{patron_id}", response_model=PatronRead)
def get_a_patron(patron_id: int, db: Session = Depends(get_session)):
    return read_patron(patron_id=patron_id, db=db)


@router.patch("/{patron_id}", response_model=PatronRead)
def update_a_patron(
    patron_id: int, patron: PatronUpdate, db: Session = Depends(get_session)
):
    return update_patron(patron_id=patron_id, patron=patron, db=db)


@router.delete("/{patron_id}")
def delete_a_patron(patron_id: int, db: Session = Depends(get_session)):
    return delete_patron(patron_id=patron_id, db=db)
