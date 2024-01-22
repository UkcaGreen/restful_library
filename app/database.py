from sqlmodel import Session, SQLModel, create_engine

from config import settings

connect_args = {}
engine = create_engine(settings.DATABASE_URI, echo=True, connect_args=connect_args)


def create_db_and_tables():
    from public.book.models import Book
    from public.patron.models import Patron
    from public.operations.models import Checkout

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session