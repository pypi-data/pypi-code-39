import os

import pytest

from auger.cli.cli import cli
from auger.api.cloud.rest_api import RestApi
from auger.api.credentials import Credentials

from .utils import interceptor


class TestAuthCLI():
    def test_login(self, log, runner, isolated, monkeypatch):
        PAYLOAD = {
            'create_token': {
                'data': {
                    'token': 'fake_token_for_testing_purpose',
                    },
            },
            'get_organizations': {
                'meta': {
                    'status': 200,
                    'pagination':
                        {'limit': 100, 'total': 1, 'count': 1, 'offset': 0}
                },
                'data': [{'name': 'auger'}]
            }
        }
        interceptor(PAYLOAD, monkeypatch)
        monkeypatch.setenv("AUGER_CREDENTIALS_PATH", os.getcwd())
        result = runner.invoke(
            cli,
            ['auth', 'login'],
            input="test@example.com\nauger\npassword\n")
        assert result.exit_code == 0
        assert (log.records[-1].message ==
                "You are now logged in on https://app.auger.ai"
                " as test@example.com.")

    def test_logout(self, log, runner, isolated, monkeypatch, authenticated):
        result = runner.invoke(cli, ['auth', 'logout'])
        assert result.exit_code == 0
        assert log.records[-1].message == "You are logged out of Auger."

    def test_whoami_anonymous(self, log, runner, monkeypatch):
        monkeypatch.setenv("AUGER_CREDENTIALS", '{}')
        result = runner.invoke(cli, ['auth', 'whoami'])
        assert result.exit_code != 0
        assert (log.records[-1].message ==
                "Please login to Auger...")

    def test_whoami_authenticated(self, log, runner, monkeypatch, authenticated):
        result = runner.invoke(cli, ['auth', 'whoami'])
        assert result.exit_code == 0
        assert (log.records[-1].message ==
                "test_user auger https://example.com")

    def test_logout_not_logged(self, log, runner, isolated, monkeypatch):
        monkeypatch.setenv("AUGER_CREDENTIALS", '{}')
        result = runner.invoke(cli, ['auth', 'logout'])
        assert (log.records[-1].message == 'You are not logged in Auger.')
        assert result.exit_code != 0
