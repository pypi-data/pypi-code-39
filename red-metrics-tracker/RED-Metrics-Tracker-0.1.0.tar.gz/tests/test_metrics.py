import pytest

from prometheus_client import Counter, Histogram

from red.metrics import HTTP_REQUESTS_LATENCY, HTTP_REQUESTS_TOTAL, HTTP_EXCEPTIONS_TOTAL


class TestMetricsTypes:

    @pytest.mark.parametrize(
        "metric, expected_type",
        argvalues=[
            (HTTP_REQUESTS_TOTAL, Counter),
            (HTTP_EXCEPTIONS_TOTAL, Counter),
            (HTTP_REQUESTS_LATENCY, Histogram)
        ]
    )
    def test_metrics_have_the_correct_types(self, metric, expected_type):
        assert isinstance(metric, expected_type)

