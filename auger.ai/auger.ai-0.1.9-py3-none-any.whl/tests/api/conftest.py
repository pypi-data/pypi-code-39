import pytest


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    def request(*args, **kwargs):
        raise Exception("No way further")
        return {}
    monkeypatch.setattr('requests.sessions.Session.request', request)
