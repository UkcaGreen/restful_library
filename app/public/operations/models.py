from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from pydantic import validator


class CheckoutBase(SQLModel):
    checkout_date: datetime
    expected_return_date: datetime | None
    return_date: datetime | None = None


class Checkout(CheckoutBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    patron_id: int = Field(default=None, foreign_key="patron.id")
    patron: "Patron" = Relationship(back_populates="checkouts") # type: ignore

    book_id: int = Field(default=None, foreign_key="book.id")
    book: "Book" = Relationship(back_populates="checkouts") # type: ignore


class CheckoutCreate(CheckoutBase):
    patron_id: int
    book_id: int


class CheckoutReturn(SQLModel):
    patron_id: int
    book_id: int


class CheckoutRead(CheckoutBase):
    id: int
    patron_id: int
    book_id: int