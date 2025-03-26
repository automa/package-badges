from functools import lru_cache

from sentry_sdk import init
from sentry_sdk.integrations.logging import LoggingIntegration

from .env import env, environment, isProduction, product, service, version


@lru_cache
def init_error_tracking():
    isErrorTrackingEnabled = isProduction and bool(env().sentry_dsn)

    if isErrorTrackingEnabled:
        init(
            dsn=env().sentry_dsn,
            release=f"{product}-{service}@{version}",
            environment=environment,
            integrations=[LoggingIntegration(event_level=None)],
        )


init_error_tracking()
