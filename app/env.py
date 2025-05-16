import os
import tomllib
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

pyproject_file = Path(__file__).parent.parent / "pyproject.toml"
pyproject_data = tomllib.load(open(pyproject_file, "rb"))

environment = os.getenv("PYTHON_ENV", "development")

isTest = environment == "test"
isProduction = not isTest and environment != "development"

product = "bots"
service = "package-badges"
version = pyproject_data["project"]["version"]


# TODO: Nested env not supported with single underscore
class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    automa_webhook_secret: str = "atma_whsec_package-badges"
    sentry_dsn: str = ""


@lru_cache
def env():
    return Config()
