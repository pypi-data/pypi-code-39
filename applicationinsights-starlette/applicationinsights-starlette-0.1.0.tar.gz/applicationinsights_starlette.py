import datetime

from applicationinsights import TelemetryClient
from applicationinsights.channel import AsynchronousSender
from applicationinsights.channel import AsynchronousQueue
from applicationinsights.channel import TelemetryChannel
from applicationinsights.logging import LoggingHandler
from starlette.requests import Request


class AppInsights:
    def __init__(self, key):
        sender = AsynchronousSender()

        queue = AsynchronousQueue(sender)
        self._channel = TelemetryChannel(None, queue)

        self._trace_log_handler = LoggingHandler(key, telemetry_channel=self._channel)
        self._exception_telemetry_client = TelemetryClient(key, telemetry_channel=self._channel)
        self._requests_telemetry_client = TelemetryClient(key, telemetry_channel=self._channel)

    @property
    def log_handler(self):
        return self._trace_log_handler

    async def exception_handler(self, _: Request, exception):
        self._exception_telemetry_client.track_exception()
        raise exception

    async def flush_middleware(self, request: Request, call_next):
        response = await call_next(request)

        self._exception_telemetry_client.flush()
        self._trace_log_handler.flush()
        self._requests_telemetry_client.flush()
        return response

    async def request_middleware(self, request: Request, call_next):
        start_time = datetime.datetime.utcnow()

        response = await call_next(request)

        end_time = datetime.datetime.utcnow()
        duration = int((end_time - start_time).total_seconds() * 1000)

        self._requests_telemetry_client.track_request(
           request.url.path, str(request.url), response.status_code < 400,
           start_time.isoformat() + 'Z', duration, response.status_code,
           request.method)
        return response
