import os
import secrets
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "RESTful Library"
    DESCRIPTION: str = "A FastAPI application with RESTful API endpoints for managing library operations."
    ENV: Literal["development", "staging", "production"] = os.environ.get("ENV")
    VERSION: str = "0.1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URI: str = os.environ.get("DATABASE_URI")
    API_USERNAME: str = os.environ.get("API_USERNAME")
    API_PASSWORD: str = os.environ.get("API_PASSWORD")

    model_config = SettingsConfigDict(
        case_sensitive=True,
    )


settings = Settings()