import os
import typing as t
import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.environ.get('CONFIG_PATH', os.path.join(BASE_DIR, 'local.env'))
load_dotenv(dotenv_path=CONFIG_PATH, verbose=True)


default_route: str = "/traffic-info"
sentry_sdk.init(
    integrations=[
        StarletteIntegration(transaction_style="endpoint"),
        FastApiIntegration(transaction_style="endpoint"),
    ],
)


def database_uri() -> str:
    """db connection"""
    db_host = os.getenv("MONGODB_HOSTNAME", "localhost")
    db_port = os.getenv("MONGODB_PORT", "27017")
    db_name = os.getenv("MONGODB_NAME", "traffic")
    db_username = os.getenv("MONGODB_USERNAME")
    db_password = os.getenv("MONGODB_PASSWORD")

    client_setup = (
        f"mongodb://{db_username}:{db_password}@{db_host}:{db_port}/?authMechanism=DEFAULT&authSource={db_name}"
    )

    return client_setup


class Settings(BaseSettings):
    """app config settings"""

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "traffic-info")
    VERSION: t.Optional[str]
    DESCRIPTION: t.Optional[str]
    SECRET_KET: t.Optional[str]
    DEBUG: bool = bool(os.getenv("DEBUG", "False"))
    ENVIRONMENT: t.Optional[str] = os.getenv("ENVIRONMENT")
    DB_URI: str = database_uri()

    class Config:
        case_sensitive = True


@lru_cache
def get_config() -> Settings:
    return Settings()
