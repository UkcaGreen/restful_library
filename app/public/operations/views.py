from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from public.operations import crud
from public.operations.models import CheckoutCreate, CheckoutRead, CheckoutReturn

router = APIRouter()


@router.post("/checkout", response_model=CheckoutRead)
def checkout_a_book(checkout: CheckoutCreate, db: Session = Depends(get_session)):
    return crud.checkout_a_book(checkout=checkout, db=db)


@router.post("/return", response_model=CheckoutRead)
def return_a_book(return_details: CheckoutReturn, db: Session = Depends(get_session)):
    return crud.return_a_book(return_details=return_details, db=db)
