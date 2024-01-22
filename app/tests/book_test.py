from tests.fixtures import session_fixture, authenticated_client_fixture
from fastapi.testclient import TestClient
import pytest


@pytest.fixture(name="populate_book")
def populate_book_fixture(authenticated_client: TestClient):
    authenticated_client.post(
        "/books/",
        json={
            "title": "Gece",
            "author": "Bilge Karasu",
            "release_date": "1985-01-01T00:00:00",
        },
    )
    authenticated_client.post(
        "/books/",
        json={
            "title": "Satranç",
            "author": "Stefan Zweig",
            "release_date": "1942-01-01T00:00:00",
        },
    )


def test_create_book(authenticated_client: TestClient, populate_book):
    response = authenticated_client.post(
        "/books/",
        json={
            "title": "Simyacı",
            "author": "Paulo Coelho",
            "release_date": "1998-01-01T00:00:00",
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Simyacı"
    assert data["author"] == "Paulo Coelho"
    assert data["release_date"] == "1998-01-01T00:00:00"
    assert data["id"] is not None


def test_update_book(authenticated_client: TestClient, populate_book):
    response = authenticated_client.patch(
        f"/books/{1}",
        json={
            "title": "GECE",
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "GECE"
    assert data["author"] == "Bilge Karasu"
    assert data["release_date"] == "1985-01-01T00:00:00"
    assert data["id"] is not None


def test_get_book(authenticated_client: TestClient, populate_book):
    response = authenticated_client.get(f"/books/{1}")

    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Gece"
    assert data["author"] == "Bilge Karasu"
    assert data["release_date"] == "1985-01-01T00:00:00"
    assert data["id"] is not None


def test_get_books(authenticated_client: TestClient, populate_book):
    response = authenticated_client.get(f"/books/")

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2


def test_delete_book(authenticated_client: TestClient, populate_book):
    response = authenticated_client.delete(f"/books/{1}")

    data = response.json()

    assert response.status_code == 200
    assert data["ok"] == True
