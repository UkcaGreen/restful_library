from celery import Celery
from celery.schedules import crontab
from database import create_db_and_tables, get_session
from datetime import datetime, timedelta
from utils.email import send_email

from public.operations.models import Checkout
from public.book.models import Book
from public.patron.models import Patron
from sqlmodel import select
import pandas as pd

import os

create_db_and_tables()
app = Celery(
    "celery_tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=1, minute=0, day_of_week=1),  # every Monday at 1:00 a.m.
        create_weekly_report.s(),
    )

    sender.add_periodic_task(
        crontab(hour=6, minute=0),  # every day at 6:00 a.m.
        send_reminder_emails_for_overdue_books.s(),
    )


@app.task
def create_weekly_report() -> list[dict]:
    with next(get_session()) as db:
        results = db.exec(
            select(Checkout, Book, Patron)
            .where(Checkout.book_id == Book.id)
            .where(Checkout.patron_id == Patron.id)
            .where(Checkout.checkout_date > datetime.utcnow() - timedelta(days=7))
        ).all()

        print(results)

        records = []

        for checkout, book, patron in results:
            checkout_dict = {
                f"checkout__{k}": v for k, v in checkout.model_dump().items()
            }
            book_dict = {f"book__{k}": v for k, v in book.model_dump().items()}
            patron_dict = {f"patron__{k}": v for k, v in patron.model_dump().items()}

            records.append(checkout_dict | book_dict | patron_dict)

    df = pd.DataFrame(records)
    df.to_csv(f"/reports/{datetime.utcnow().isoformat()}")

    return df.to_dict("records")


@app.task
def send_reminder_emails_for_overdue_books() -> bool:
    with next(get_session()) as db:
        over_due_checkouts = db.exec(
            select(Checkout).where(Checkout.expected_return_date < datetime.utcnow())
        ).all()

        for checkout in over_due_checkouts:
            book, patron = checkout.book, checkout.patron

            send_email(
                title="Over Due Book",
                body=f"There is an over due book titled {book.title}, in your name.",
                to_email=patron.email,
                from_email=os.environ.get("FROM_EMAIL"),
                password=os.environ.get("FROM_EMAIL_PASSWORD"),
            )

    return True
