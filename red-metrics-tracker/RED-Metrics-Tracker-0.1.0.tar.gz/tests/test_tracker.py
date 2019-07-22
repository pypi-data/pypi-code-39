import time

import flask
import pytest
from prometheus_client import REGISTRY
from werkzeug.exceptions import Unauthorized

from red import REDMetricsTracker


def construct_test_app():
    app = flask.Flask(__name__)

    app.config["TESTING"] = True

    def view_func():
        if flask.request.method == "PUT":
            # Should be ignored, passed up to flask and converted to a 500 Error.
            raise ValueError

        if flask.request.method == "DELETE":
            print("waiting a few seconds..")
            time.sleep(2)

        if flask.request.method == "POST":
            # Should be tracked, and passed up to flask and raised as is.
            raise Unauthorized

        return "OK"

    @app.route("/test/defaults", methods=["POST", "GET", "PUT", "DELETE"])
    @REDMetricsTracker.track()
    def test_view_defaults():
        return view_func()

    @app.route("/test/only-specific-exc", methods=["POST", "GET", "PUT", "DELETE"])
    @REDMetricsTracker.track(exc=Unauthorized)
    def test_view_spec_exc():
        return view_func()

    @app.route("/test/only-specific-method", methods=["POST", "GET", "PUT", "DELETE"])
    @REDMetricsTracker.track(method="POST")
    def test_view_spec_method():
        return view_func()

    return app


@pytest.fixture
def app():
    return construct_test_app()


@pytest.fixture
def client(app):
    return app.test_client()


class TestREDMetricsDefaults:

    def test_requests_made_counter(self, client):
        method, path = 'GET', '/test/defaults'
        before = REGISTRY.get_sample_value('http_requests_total', {'method': method, 'path': path}) or 0
        assert before == 0

        client.get("/test/defaults")

        after = REGISTRY.get_sample_value('http_requests_total', {'method': method, 'path': path})
        assert after is not None
        assert after == 1

    def test_requests_exceptions_counter(self, client):
        method, path = 'PUT', '/test/defaults'
        before = REGISTRY.get_sample_value('http_exceptions_total', {'method': method, 'path': path}) or 0
        assert before == 0

        try:
            client.put("/test/defaults")
        except:
            pass

        after = REGISTRY.get_sample_value('http_exceptions_total', {'method': method, 'path': path})
        assert after is not None
        assert after - before == 1

    def test_request_latency_count(self, client):
        method, path = 'DELETE', '/test/defaults'
        before = REGISTRY.get_sample_value('http_requests_latency_seconds_count', {'method': method, 'path': path}) or 0
        assert before == 0

        client.delete("/test/defaults")

        after = REGISTRY.get_sample_value('http_requests_latency_seconds_count', {'method': method, 'path': path})
        assert after is not None
        assert after - before == 1


class TestREDMetricsMethodFilter:

    def test_requests_made_counter_is_not_incremented_for_non_tracked_metrics(self, client):
        method, path = "POST", '/test/defaults'
        before = REGISTRY.get_sample_value('http_requests_total', {'method': method, 'path': path}) or 0
        assert before == 0

        try:
            client.post("/test/only-specific-method")
        except:
            pass

        after = REGISTRY.get_sample_value('http_requests_total', {'method': method, 'path': path})

        assert after == 1

    @pytest.mark.parametrize("method", ["GET", "PUT", "DELETE"])
    def test_requests_made_counter_is_not_incremented_for_non_tracked_metrics(self, method, client):
        path = '/test/only-specific-method'
        before = REGISTRY.get_sample_value('http_requests_total', {'method': method, 'path': path}) or 0

        try:
            getattr(client, method.lower())("/test/only-specific-method")
        except:
            pass

        after = REGISTRY.get_sample_value('http_requests_total', {'method': method, 'path': path}) or 0
        assert before == after


class TestREDMetricsExceptionFilter:

    @pytest.mark.parametrize("method, trigger_exc", [("PUT", False), ("POST", True)])
    def test_exceptions_counter_is_incremented_for_tracked_exceptions_only(self, method, trigger_exc, client):
        method, path = method, '/test/only-specific-exc'
        before = REGISTRY.get_sample_value('http_exceptions_total', {'method': method, 'path': path}) or 0
        assert before == 0

        try:
            getattr(client, method.lower())("/test/only-specific-exc")
        except:
            pass

        after = REGISTRY.get_sample_value('http_exceptions_total', {'method': method, 'path': path}) or 0

        assert after == int(trigger_exc)
