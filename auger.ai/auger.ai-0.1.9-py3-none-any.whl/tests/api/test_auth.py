import pytest

from auger.api.cloud.auth import AugerAuthApi
from auger.api.utils.context import Context
from auger.api.cloud.utils.exception import AugerException
from .utils import interceptor


class TestLogin():
    def setup_method(self):
        self.ctx = Context()
        self.auth_api = AugerAuthApi(self.ctx)

    def test_success(self, monkeypatch):
        PAYLOAD = {
            'create_token': {
                'data': {
                    'token': 'fake_token',
                    'confirmation_required': False}
            },
            'get_organizations': {
                'meta': {
                    'pagination': {
                        'offset': 0, 'limit': 100, 'total': 1, 'count': 1},
                     'status': 200},
                'data': [
                    {'name': 'test_org_name',}
                ]
            }

        }
        interceptor(PAYLOAD, monkeypatch)
        token = self.auth_api.login(
            'username', 'password', 'test_org_name', 'localhost')
        assert token == 'fake_token'

    def test_incorrect(self, monkeypatch):
        def mock(*args, **kwargs):
            raise AugerException('Email or password incorrect')
        monkeypatch.setattr('auger.api.cloud.rest_api.RestApi.call_ex', mock)
        with pytest.raises(AugerException) as excinfo:
            token = self.auth_api.login(
                'username', 'wrong_pass', 'test_org_name', 'localhost')
        assert "Email or password incorrect" in str(excinfo.value)

    def test_organization_doesnt_exist(self, monkeypatch):
        PAYLOAD = {
            'create_token': {
                'data': {
                    'token': 'fake_token',
                    'confirmation_required': False}
            },
            'get_organizations': {
                'meta': {
                    'pagination': {
                        'offset': 0, 'limit': 100, 'total': 0, 'count': 0},
                     'status': 200},
                'data': []
            }
        }
        interceptor(PAYLOAD, monkeypatch)
        with pytest.raises(AugerException) as excinfo:
            token = self.auth_api.login(
                'username', 'password', 'non_existing_org', 'localhost')
        assert (str(excinfo.value) ==
            "Auger Organization non_existing_org doesn't exist")
