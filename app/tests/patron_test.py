from tests.fixtures import session_fixture, authenticated_client_fixture
from fastapi.testclient import TestClient
import pytest


@pytest.fixture(name="populate_patron")
def populate_patron_fixture(authenticated_client: TestClient):
    authenticated_client.post(
        "/patrons/",
        json={
            "username": "Ali Yılmaz",
            "email": "library_case_study@outlook.com",
        },
    )
    authenticated_client.post(
        "/patrons/",
        json={
            "username": "Veli Özcan",
            "email": "library_case_study@outlook.com",
        },
    )


def test_create_patron(authenticated_client: TestClient, populate_patron):
    response = authenticated_client.post(
        "/patrons/",
        json={
            "username": "Ayşe Bakar",
            "email": "library_case_study@outlook.com",
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["username"] == "Ayşe Bakar"
    assert data["email"] == "library_case_study@outlook.com"


def test_update_patron(authenticated_client: TestClient, populate_patron):
    response = authenticated_client.patch(
        f"/patrons/{1}",
        json={
            "username": "Ali Yılar",
        },
    )

    data = response.json()

    print(data)

    assert response.status_code == 200
    assert data["username"] == "Ali Yılar"
    assert data["email"] == "library_case_study@outlook.com"
    assert data["id"] is not None


def test_get_patron(authenticated_client: TestClient, populate_patron):
    response = authenticated_client.get(f"/patrons/{1}")

    data = response.json()

    assert response.status_code == 200
    assert data["username"] == "Ali Yılmaz"
    assert data["email"] == "library_case_study@outlook.com"
    assert data["id"] is not None


def test_get_patrons(authenticated_client: TestClient, populate_patron):
    response = authenticated_client.get(f"/patrons/")

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2


def test_delete_patron(authenticated_client: TestClient, populate_patron):
    response = authenticated_client.delete(f"/patrons/{1}")

    data = response.json()

    assert response.status_code == 200
    assert data["ok"] == True
