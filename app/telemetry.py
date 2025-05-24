import atexit
import logging
from functools import lru_cache

from opentelemetry import _logs, metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
    ConsoleLogExporter,
    SimpleLogRecordProcessor,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
)
from opentelemetry.semconv._incubating.attributes.deployment_attributes import (
    DEPLOYMENT_ENVIRONMENT_NAME,
)
from opentelemetry.semconv._incubating.attributes.service_attributes import (
    SERVICE_NAME,
    SERVICE_NAMESPACE,
    SERVICE_VERSION,
)

from .env import environment, isProduction, isTest, product, service, version


@lru_cache
def initTelemetry():
    resource = Resource.create(
        {
            SERVICE_NAMESPACE: product,
            SERVICE_NAME: service,
            SERVICE_VERSION: version,
            DEPLOYMENT_ENVIRONMENT_NAME: environment,
        }
    )

    # Traces
    trace_provider = TracerProvider(resource=resource)

    if not isTest:
        if isProduction:
            trace_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
        else:
            trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))

    trace.set_tracer_provider(trace_provider)

    # Logs
    logger_provider = LoggerProvider(resource=resource)

    if not isTest:
        if isProduction:
            logger_provider.add_log_record_processor(
                BatchLogRecordProcessor(ConsoleLogExporter())
            )
        else:
            logger_provider.add_log_record_processor(
                SimpleLogRecordProcessor(ConsoleLogExporter())
            )

    logging_handler = LoggingHandler(
        level=logging.NOTSET, logger_provider=logger_provider
    )

    logging.getLogger().addHandler(logging_handler)
    _logs.set_logger_provider(logger_provider)

    # Metrics
    metric_readers = []

    if not isTest:
        metric_readers.append(PeriodicExportingMetricReader(OTLPMetricExporter()))

    meter_provider = MeterProvider(resource=resource, metric_readers=metric_readers)

    metrics.set_meter_provider(meter_provider)

    # Instrumentation
    FastAPIInstrumentor().instrument()

    def shutdownTelemetry():
        trace_provider.shutdown()
        logger_provider.shutdown()
        meter_provider.shutdown()

        print("Telemetry shut down successfully")

    # Register shutdown handler
    atexit.register(shutdownTelemetry)


initTelemetry()


tracer = trace.get_tracer("default")

logger = logging.getLogger("uvicorn")

meter = metrics.get_meter("default")
