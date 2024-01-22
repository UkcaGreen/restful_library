from tests.fixtures import session_fixture, authenticated_client_fixture
from tests.book_test import populate_book_fixture
from tests.patron_test import populate_patron_fixture
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import pytest

TEST_CHECKOUTS = [
    {
        "checkout_date": (datetime.utcnow() - timedelta(days=3)).replace(second=0, microsecond=0).isoformat(),
        "expected_return_date": (datetime.utcnow() - timedelta(days=1)).replace(second=0, microsecond=0).isoformat(),
        "patron_id": 1,
        "book_id": 1
    },
    {
        "checkout_date": (datetime.utcnow() - timedelta(days=3)).replace(second=0, microsecond=0).isoformat(),
        "expected_return_date": (datetime.utcnow() + timedelta(days=10)).replace(second=0, microsecond=0).isoformat(),
        "return_date": (datetime.utcnow() - timedelta(days=1)).replace(second=0, microsecond=0).isoformat(),
        "patron_id": 1,
        "book_id": 2
    },
    {
        "checkout_date": datetime.utcnow().isoformat(),
        "expected_return_date": (datetime.utcnow() + timedelta(days=3)).isoformat(),
        "patron_id": 2,
        "book_id": 2
    },
]

@pytest.fixture(name="populate_checkout")
def populate_checkout_fixture(authenticated_client: TestClient, populate_book, populate_patron):
    authenticated_client.post("/operations/checkout/", json=TEST_CHECKOUTS[0])
    authenticated_client.post("/operations/checkout/", json=TEST_CHECKOUTS[1])


def test_checkout_operation(authenticated_client: TestClient, populate_checkout):

    response = authenticated_client.post("/operations/checkout/", json=TEST_CHECKOUTS[2])
    data = response.json()

    assert response.status_code == 200
    assert data["checkout_date"] == TEST_CHECKOUTS[2]["checkout_date"]
    assert data["expected_return_date"] == TEST_CHECKOUTS[2]["expected_return_date"]
    assert data["patron_id"] == TEST_CHECKOUTS[2]["patron_id"]
    assert data["book_id"] == TEST_CHECKOUTS[2]["book_id"] 
    assert data["return_date"] == None


def test_return_operation(authenticated_client: TestClient, populate_checkout):

    response = authenticated_client.post(
        "/operations/return/", json={
            "patron_id": 1,
            "book_id": 1
        }
    )
    data = response.json()

    assert response.status_code == 200
    assert data["checkout_date"] == TEST_CHECKOUTS[0]["checkout_date"]
    assert data["expected_return_date"] == TEST_CHECKOUTS[0]["expected_return_date"]
    assert data["patron_id"] == TEST_CHECKOUTS[0]["patron_id"]
    assert data["book_id"] == TEST_CHECKOUTS[0]["book_id"] 
    assert data["return_date"] != None


def test_read_overdue_books(authenticated_client: TestClient, populate_checkout):

    response = authenticated_client.get("/books/over_due/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1


def test_read_checked_out_books(authenticated_client: TestClient, populate_checkout):

    response = authenticated_client.get("/books/checked_out/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1