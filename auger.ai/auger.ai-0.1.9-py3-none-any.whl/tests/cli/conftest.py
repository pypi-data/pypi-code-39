import logging
import shutil
import os
import json

import pytest
from click.testing import CliRunner

from auger.api.credentials import Credentials
from auger.api.cloud.rest_api import RestApi

TEST_CREDENTIALS = {
    'username': 'test_user',
    'organization': 'auger',
    'url': 'https://example.com',
    'token': 'fake_token',
}

@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(scope="function")
def isolated(runner):
    with runner.isolated_filesystem():
        yield runner


@pytest.fixture
def log(caplog):
    caplog.set_level(logging.INFO)
    return caplog


@pytest.fixture
def project(isolated):
    source = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'fixtures',
        'test_project')
    shutil.copytree(source, './test_project')
    os.chdir('test_project')


@pytest.fixture
def authenticated(monkeypatch, isolated):
    monkeypatch.setenv("AUGER_CREDENTIALS", json.dumps(TEST_CREDENTIALS))
    monkeypatch.setenv("AUGER_CREDENTIALS_PATH", os.getcwd())


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    def request(*args, **kwargs):
        print("CALLED HubApiClient.request(", args, kwargs, ")")
        raise Exception("No way further")
        return {}
    monkeypatch.setattr('auger.hub_api_client.HubApiClient.request', request)
