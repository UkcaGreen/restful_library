from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy import func

from database import get_session
from public.operations.models import Checkout, CheckoutCreate, CheckoutReturn
from public.book.crud import read_book
from public.patron.crud import read_patron

from datetime import datetime


def checkout_a_book(checkout: CheckoutCreate, db: Session = Depends(get_session)) -> Checkout:

    # check if both book and patron exists
    read_book(checkout.book_id, db)
    read_patron(checkout.patron_id, db)

    # check if book is already checked out
    result = db.exec(
        select(func.count(Checkout.id))
        .where(Checkout.book_id == checkout.book_id)
        .where(Checkout.return_date == None)
    ).one()

    if result != 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book is not available with id: {checkout.book_id}",
        )

    checkout = Checkout.model_validate(checkout)
    db.add(checkout)
    db.commit()
    db.refresh(checkout)
    return checkout

def return_a_book(return_details: CheckoutReturn, db: Session = Depends(get_session)) -> Checkout:
    
    # check if both book and patron exists
    read_book(return_details.book_id, db)
    read_patron(return_details.patron_id, db)

    # check if book is checked out by the mentioned patron
    checkout = db.exec(
        select(Checkout)
        .where(Checkout.book_id == return_details.book_id)
        .where(Checkout.patron_id == return_details.patron_id)
        .where(Checkout.return_date == None)
    ).one_or_none()

    if not checkout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Checkout not found with book_id: {return_details.book_id} and patron_id: {return_details.patron_id}",
        )

    patch = return_details.model_dump(exclude_unset=True)
    for key, value in patch.items():
        setattr(checkout, key, value)

    setattr(checkout, "return_date", datetime.utcnow())

    db.add(checkout)
    db.commit()
    db.refresh(checkout)
    return checkout
