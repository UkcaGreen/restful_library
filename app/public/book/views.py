from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from database import get_session
from public.book.crud import (
    create_book,
    delete_book,
    read_book,
    read_books,
    update_book,
    read_checked_out_books,
    read_over_due_books,
)
from public.book.models import BookCreate, BookRead, BookUpdate

router = APIRouter()


@router.post("", response_model=BookRead)
def create_a_book(book: BookCreate, db: Session = Depends(get_session)):
    return create_book(book=book, db=db)


@router.get("", response_model=list[BookRead])
def get_books(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    return read_books(offset=offset, limit=limit, db=db)


@router.get("/{book_id}", response_model=BookRead)
def get_a_book(book_id: int, db: Session = Depends(get_session)):
    return read_book(book_id=book_id, db=db)


@router.patch("/{book_id}", response_model=BookRead)
def update_a_book(book_id: int, book: BookUpdate, db: Session = Depends(get_session)):
    return update_book(book_id=book_id, book=book, db=db)


@router.delete("/{book_id}")
def delete_a_book(book_id: int, db: Session = Depends(get_session)):
    return delete_book(book_id=book_id, db=db)


@router.get("/checked_out/", response_model=list[BookRead])
def get_checked_out_books(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    return read_checked_out_books(offset=offset, limit=limit, db=db)


@router.get("/over_due/", response_model=list[BookRead])
def get_over_due_books(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    return read_over_due_books(offset=offset, limit=limit, db=db)
