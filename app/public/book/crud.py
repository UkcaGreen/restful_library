from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from public.book.models import Book, BookCreate, BookUpdate
from public.operations.models import Checkout

from typing import Sequence
from datetime import datetime


def create_book(book: BookCreate, db: Session = Depends(get_session)) -> Book:
    book = Book.model_validate(book)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def read_books(
    offset: int = 0, limit: int = 20, db: Session = Depends(get_session)
) -> Sequence[Book]:
    books = db.exec(select(Book).offset(offset).limit(limit)).all()
    return books


def read_book(book_id: int, db: Session = Depends(get_session)) -> Book:
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book not found with id: {book_id}",
        )
    return book


def update_book(
    book_id: int, book: BookUpdate, db: Session = Depends(get_session)
) -> Book:
    book_to_update = db.get(Book, book_id)
    if not book_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book not found with id: {book_id}",
        )

    patch = book.model_dump(exclude_unset=True)
    for key, value in patch.items():
        setattr(book_to_update, key, value)

    db.add(book_to_update)
    db.commit()
    db.refresh(book_to_update)
    return book_to_update


def delete_book(book_id: int, db: Session = Depends(get_session)) -> dict:
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book not found with id: {book_id}",
        )

    db.delete(book)
    db.commit()
    return {"ok": True}


def read_checked_out_books(
    offset: int = 0, limit: int = 20, db: Session = Depends(get_session)
) -> Sequence[Book]:
    statement = (
        select(Checkout, Book)
        .where(Checkout.book_id == Book.id)
        .where(Checkout.return_date == None)
    )
    results = db.exec(statement)
    books = [book for checkout, book in results]
    return books


def read_over_due_books(
    offset: int = 0, limit: int = 20, db: Session = Depends(get_session)
) -> Sequence[Book]:
    statement = (
        select(Checkout, Book)
        .where(Checkout.book_id == Book.id)
        .where(Checkout.expected_return_date < datetime.utcnow())
        .where(Checkout.return_date == None)
    )
    results = db.exec(statement)
    books = [book for checkout, book in results]
    return books
