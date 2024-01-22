from tests.fixtures import session_fixture, authenticated_client_fixture
from tests.book_test import populate_book_fixture
from tests.patron_test import populate_patron_fixture
from tests.checkout_test import populate_checkout_fixture
from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch
from sqlmodel import Session
import os


@pytest.fixture(name="patched_session")
def patched_session(mocker, session: Session):
    def get_session_override():  
        yield session

    mocker.patch('database.create_db_and_tables', return_value=True)
    mocker.patch('database.get_session', get_session_override)

    return session
    

def test_create_weekly_report(populate_checkout, mocker, patched_session: Session):

    mocker.patch('pandas.DataFrame.to_csv', return_value=None)

    from celery_tasks import create_weekly_report

    records = create_weekly_report()

    assert len(records) == 2


def test_send_reminder_emails_for_overdue_books(populate_checkout, patched_session: Session):

    from celery_tasks import send_reminder_emails_for_overdue_books

    os.environ["FROM_EMAIL"] = "library_case_study@outlook.com"
    os.environ["FROM_EMAIL_PASSWORD"] = "XQXy=heq)_&3rGk"

    records = send_reminder_emails_for_overdue_books()

    