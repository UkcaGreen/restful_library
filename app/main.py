from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import Settings, settings
from database import create_db_and_tables
from public import api as public_api
from utils.logger import create_custom_logger

logger = create_custom_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    logger.info("startup: triggered")

    yield

    logger.info("shutdown: triggered")


def create_app(settings: Settings):
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/",
        description=settings.DESCRIPTION,
        lifespan=lifespan,
    )

    app.include_router(public_api)

    return app


api = create_app(settings)
