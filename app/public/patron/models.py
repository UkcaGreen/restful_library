from sqlmodel import Field, Relationship, SQLModel

from public.book.models import Book


class PatronBase(SQLModel):
    username: str
    email: str


class Patron(PatronBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    checkouts: list["Checkout"] = Relationship(back_populates="patron")  # type: ignore


class PatronCreate(PatronBase):
    pass


class PatronRead(PatronBase):
    id: int
    username: str | None = None
    email: str | None = None

    books: list | None = None


class PatronUpdate(PatronBase):
    username: str | None = None
    email: str | None = None
