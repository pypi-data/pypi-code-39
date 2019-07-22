"""Prometheus Metrics used to monitor URL views.

Available metrics are:

    http_requests_total
        The total number of requests made to the application.

    http_exceptions_total
        The total number of exceptions raised during processing or requests. Please
        note that *404 Not Found* errors caused by requesting incorrect URLs are **NOT**
        included in this metric, since they are raised during routing, before the
        execution of any of our endpoint functions.

        However, `404 Not Found` exceptions raised explicitly by our functions
        are monitored.

    http_requests_latency_seconds
        The number of seconds required to process requests to endpoints of the
        application.

All of the above metrics offer `path` and `method` labels for more granular filtering
using PromQL.
"""
from prometheus_client import Counter, Histogram

#: Counter Metric, counting all requests made and processed by a decorated view. This
#: is regardless of whether or not there was an exception during the request of that view.
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total", "Total amount of HTTP Requests made.", labelnames=["method", "path"]
)

#: Tracks if an exception occurred during the execution of the decorated view. Note that any
#: `404 Not Found` errors which happen during routing are NOT part of this metric, as the corresponding
#: exceptions happens during routing, and not in this view. Any `404 Not Found` exceptions
#: raised explicitly in the view are still counted towards this metric.
HTTP_EXCEPTIONS_TOTAL = Counter(
    "http_exceptions_total", "Total amount of HTTP exceptions.", labelnames=["method", "path"]
)

#: Tracks the amount of time it took in seconds, to process the request in the view. This
#: includes requests that resulted in an exception.
HTTP_REQUESTS_LATENCY = Histogram(
    "http_requests_latency_seconds",
    "Duration of HTTP requests processing.",
    labelnames=["method", "path"],
)
