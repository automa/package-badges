import time
import uuid

from opentelemetry.semconv.attributes.client_attributes import (
    CLIENT_ADDRESS,
)
from opentelemetry.semconv.attributes.http_attributes import (
    HTTP_REQUEST_METHOD,
    HTTP_RESPONSE_STATUS_CODE,
)
from opentelemetry.semconv.attributes.url_attributes import URL_PATH
from starlette.middleware.base import BaseHTTPMiddleware

from ..telemetry import logger, meter

request_counter = meter.create_counter("http.request")
response_timer = meter.create_histogram("http.response_time")


class TelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        id = str(uuid.uuid4())
        start = time.time()

        request.state.request_id = id

        # TODO: We need a custom APIRoute to add the raw path to the request
        # https://github.com/encode/starlette/issues/685#issuecomment-550240999
        logger.info(
            "Incoming request",
            extra={
                "http.request.id": id,
                HTTP_REQUEST_METHOD: request.method,
                URL_PATH: request.url.path,
                CLIENT_ADDRESS: request.client.host,
            },
        )

        request_counter.add(
            1,
            {
                HTTP_REQUEST_METHOD: request.method,
                URL_PATH: request.url.path,
            },
        )

        try:
            # Forward request
            response = await call_next(request)

            response_time = time.time() - start

            logger.info(
                "Request completed",
                extra={
                    "http.request.id": id,
                    HTTP_RESPONSE_STATUS_CODE: response.status_code,
                    "http.response.time": response_time,
                },
            )

            response_timer.record(
                response_time,
                {
                    HTTP_REQUEST_METHOD: request.method,
                    URL_PATH: request.url.path,
                },
            )

            # Forward response
            return response
        except Exception as error:
            logger.error(
                "Request errored",
                extra={
                    "http.request.id": id,
                    "error.message": str(error),
                },
            )

            raise error from None
