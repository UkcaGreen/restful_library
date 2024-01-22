from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime


class BookBase(SQLModel):
    title: str
    author: str
    release_date: datetime


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    checkouts: list["Checkout"] = Relationship(back_populates="book") # type: ignore


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int
    title: str
    author: str
    release_date: datetime


class BookUpdate(BookBase):
    title: str | None = None
    author: str | None = None
    release_date: datetime | None = None