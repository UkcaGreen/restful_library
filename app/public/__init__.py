from fastapi import APIRouter, Depends

from auth import authent
from public.book import views as book_views
from public.patron import views as patron_views
from public.operations import views as operation_views

api = APIRouter()

api.include_router(
    book_views.router,
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(authent)],
)
api.include_router(
    patron_views.router,
    prefix="/patrons",
    tags=["Patrons"],
    dependencies=[Depends(authent)],
)
api.include_router(
    operation_views.router,
    prefix="/operations",
    tags=["Operations"],
    dependencies=[Depends(authent)],
)
