from pathlib import Path

from fastapi import FastAPI
from fastapi_file_router import load_routes

from .env import isProduction
from .error import *  # noqa: F403
from .plugins.error import ErrorMiddleware
from .plugins.security import SecurityMiddleware
from .plugins.telemetry import TelemetryMiddleware

app = FastAPI(openapi_url=None if isProduction else "/openapi.json")

app.add_middleware(TelemetryMiddleware)  # ty:ignore[invalid-argument-type]
app.add_middleware(ErrorMiddleware)  # ty:ignore[invalid-argument-type]
app.add_middleware(SecurityMiddleware)  # ty:ignore[invalid-argument-type]

load_routes(app, Path("./app/routes"), auto_tags=False)
