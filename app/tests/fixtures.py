from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import api
from auth import authent
from database import get_session
import pytest


@pytest.fixture(name="session")
def session_fixture():
    from public.book.models import Book
    from public.patron.models import Patron
    from public.operations.models import Checkout

    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(session: Session):
    def get_session_override():
        return session

    def skip_auth():
        return True

    api.dependency_overrides[authent] = skip_auth
    api.dependency_overrides[get_session] = get_session_override

    client = TestClient(api)
    yield client
    api.dependency_overrides.clear()
