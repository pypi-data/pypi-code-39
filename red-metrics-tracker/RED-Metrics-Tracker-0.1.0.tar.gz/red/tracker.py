"""REDMetricsTracker with :mod:`flask` support.

Tracking all methods and exceptions for all requests on a view::

    app = flask.Flask(__name__)

    @app.route("/endpoint")
    @FlaskRedMetricsTracker.track()
    def do_things():
         ...
         return "OK"

Limiting metrics tracking to specific methods::

    @app.route("/endpoint", methods=["POST", "GET", "PUT", "DELETE"])
    @FlaskRedMetricsTracker.track(methods=["POST", "DELETE"])
    def do_things():
         ...
         return "OK"

Limiting to specific exceptions::

    @app.route("/endpoint/<condition>")
    @FlaskRedMetricsTracker.track(exceptions=MySpecialException)
    def do_things():
         ...
         if condition == "throw":
            raise MySpecialException
         return "OK"
"""
import timeit

from functools import wraps
from typing import Optional, Union, Tuple, List, Type, Iterable

from flask import request


from red.metrics import HTTP_EXCEPTIONS_TOTAL, HTTP_REQUESTS_TOTAL, HTTP_REQUESTS_LATENCY


class REDMetricsTracker:
    """REDMetricsTracker class for :mod:`flask` applications.

    Dynamically looks up method and path of the request currently handled by the
    decorated view.

    Allows limiting collected metrics to certain HTTP methods, as well as specific
    exceptions.

    :param method: HTTP Method(s) to track metrics for. Defaults to all.
    :param exc: Exception(s) to track metrics for. Defaults to all exceptions raised in the view.
    """
    def __init__(
        self,
        methods: Optional[Union[str, Iterable[str]]] = None,
        exceptions: Optional[Union[Tuple[Type[Exception], ...], Type[Exception]]] = None,
    ):
        self.methods = methods
        if methods is not None:
            self.methods = [methods] if isinstance(methods, str) else methods
        self.exc = exceptions
        self.start = None
        self.last_response = None

    def __enter__(self):
        self.start = None
        if self.trackable_request:
            self.start = timeit.default_timer()
            self.total_requests.inc()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Track latency and exceptions, if any.

        Latency and exceptions are tracked if :attr:`request.method` is present in :attr:`.methods`.

        In flask, exceptions may occur in two ways:

            * Exceptions raised from user code in the view function (resulting in a 500 down stream).
            * :class:`werkzeug.exceptions.HTTPExceptions` returned by the view function.

        """
        if self.trackable_request:
            # Track the latency (request duration) of the request, in seconds.
            duration = max(timeit.default_timer() - self.start, 0)
            self.latency.observe(duration)

            # Fetch any exception that may have occurred.
            if exc_type:
                # User code raised an unhandled error (aka. 500 Internal Server Error downstream).
                exception = exc_type
            elif self.last_response:
                # The view function returned an HTTPException response.
                exception = self.last_response

            if self.trackable_exception(exception):
                self.total_exceptions.inc()
            return exc_type, exc_val, exc_tb

    @property
    def trackable_request(self) -> bool:
        """Check if the request's HTTP Verb is in the tracked methods list."""
        if self.methods is None:
            # Track all requests made to this view.
            return True
        # Only track a specific set of methods
        return request.method in self.methods

    def trackable_exception(self, exception: Type[Exception]) -> bool:
        """Check if the given `exception` is meant to be tracked.

        Returns a :class:`bool` indicating whether or not we should track the
        exception.
        """
        if self.exc is None:
            # No filter specified, track all exceptions
            return True
        elif isinstance(self.exc, Iterable):
            # We have an iterable of exceptions to filter for
            return exception in self.exc

        # We should only filter for one exception type
        return exception == self.exc

    @property
    def labels(self):
        """Loads the method, path for the current view and request.

        This accesses flask's :attr:`flask.request` thread-local variable, if
        no `method` or `path` were sent during instantiation of this instance.
        """
        return {"method": request.method, "path": request.path}

    @property
    def total_requests(self):
        """Convenience property to allow easier access to the underlying counter metric.

        Returns the metric for the configured :attr:`.labels` from
        :attr:`.HTTP_TOTAL_REQUESTS`.

        """
        return HTTP_REQUESTS_TOTAL.labels(**self.labels)

    @property
    def total_exceptions(self):
        """Convenience property to allow easier access to the underlying counter metric.

        Returns the metric for the configured :attr:`.labels` from
        :attr:`.HTTP_TOTAL_EXCEPTIONS`.
        """
        return HTTP_EXCEPTIONS_TOTAL.labels(**self.labels)

    @property
    def latency(self):
        """Convenience property to allow easier access to the underlying counter metric.

        Returns the metric for the configured :attr:`.labels` from
        :attr:`.HTTP_REQUEST_LATENCY`.
        """
        return HTTP_REQUESTS_LATENCY.labels(**self.labels)

    @classmethod
    def track(
        cls,
        method: Optional[Union[List[str], str]] = None,
        exc: Optional[Union[Tuple[Type[Exception], ...], Type[Exception]]] = None,
    ):
        """Track  RED Metrics for a  view.

        URL views decorated with this method will track
        total requests, latency and occurred exceptions.

        By default all HTTP Methods and exceptions are tracked.

        It is possible to limit this by  passing a str or list of strings in the `method` parameter,
        to limit the tracked HTTP Verbs to the given list.

        Likewise, the exceptions tracked can be limited by passing an exception class or tuple
        of several exception classes to the `exc` parameter.
        """
        def instrument_view(view_func):
            @wraps(view_func)
            def instrumented_view(*args, **kwargs):
                with cls(methods=method, exceptions=exc) as tracker:
                    resp = view_func(*args, **kwargs)
                    tracker.last_response = resp
                    return resp
            return instrumented_view
        return instrument_view
