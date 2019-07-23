import pytest
import requests_mock
from pytest import fixture

from propileu_sdk.config import HOST
from propileu_sdk.config import HOST_AUTH
from propileu_sdk.entities import base_manager as base_manager_module
from propileu_sdk.entities.base_manager import BaseManager
from propileu_sdk.entities.base_manager import _authentication_logic
from propileu_sdk.entities.exceps import PropileuSdkNotProperlyConfiguredException


@fixture
def prepare_environment(requests_mock: requests_mock.mocker.Mocker):
    requests_mock.get(
        f"{HOST}fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/",
        request_headers={"Authorization": "Token fake-token"},
        status_code=200,
        json={},
    )
    requests_mock.get(
        f"{HOST}fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/",
        request_headers={"Authorization": "Token invalid-fake-token"},
        status_code=401,
    )
    requests_mock.post(f"{HOST_AUTH}", json={"token": "fake-token"})

    yield requests_mock

    _authentication_logic.token = None


def test_should_authenticate_when_no_token_is_configured(prepare_environment):
    requests_mock = prepare_environment

    base_manager = BaseManager()
    base_manager.execute_get("fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/")

    assert len(requests_mock.request_history) == 2
    assert requests_mock.request_history[0].path == "/api/v1/api-token-auth/"
    assert requests_mock.request_history[0].text == '{"username": "admin", "password": "test"}'
    assert requests_mock.request_history[1].path == "/api/v1/fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/"


def test_should_create_new_token_when_principal_is_invalidated(prepare_environment):
    requests_mock = prepare_environment

    base_manager = BaseManager()
    base_manager.execute_get("fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/")

    assert len(requests_mock.request_history) == 2
    assert requests_mock.request_history[0].path == "/api/v1/api-token-auth/"
    assert requests_mock.request_history[0].text == '{"username": "admin", "password": "test"}'
    assert requests_mock.request_history[1].path == "/api/v1/fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/"

    base_manager.execute_get("fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/")

    assert len(requests_mock.request_history) == 3
    assert requests_mock.request_history[2].path == "/api/v1/fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/"

    base_manager.execute_get("fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/")

    assert len(requests_mock.request_history) == 4
    assert requests_mock.request_history[3].path == "/api/v1/fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/"

    # In order to simulate invalidation
    _authentication_logic.token = "invalid-fake-token"

    base_manager.execute_get("fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/")

    assert len(requests_mock.request_history) == 7
    assert requests_mock.request_history[4].path == "/api/v1/fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/"
    assert requests_mock.request_history[5].path == "/api/v1/api-token-auth/"
    assert requests_mock.request_history[5].text == '{"username": "admin", "password": "test"}'
    assert requests_mock.request_history[6].path


def test_should_raise_sdk_error_when_host_is_not_configured(monkeypatch, prepare_environment):
    monkeypatch.setattr(base_manager_module, "HOST", None)

    base_manager = BaseManager()

    with pytest.raises(PropileuSdkNotProperlyConfiguredException):
        base_manager.execute_get("fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/")


def test_should_raise_sdk_error_when_host_auth_is_not_configured(monkeypatch, prepare_environment):
    monkeypatch.setattr(base_manager_module, "HOST_AUTH", None)

    base_manager = BaseManager()

    with pytest.raises(PropileuSdkNotProperlyConfiguredException):
        base_manager.execute_get("fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/")


def test_should_raise_sdk_error_when_username_is_not_configured(monkeypatch, prepare_environment):
    monkeypatch.setattr(base_manager_module, "USERNAME", None)

    base_manager = BaseManager()

    with pytest.raises(PropileuSdkNotProperlyConfiguredException):
        base_manager.execute_get("fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/")


def test_should_raise_sdk_error_when_password_is_not_configured(monkeypatch, prepare_environment):
    monkeypatch.setattr(base_manager_module, "PASSWORD", None)

    base_manager = BaseManager()

    with pytest.raises(PropileuSdkNotProperlyConfiguredException):
        base_manager.execute_get("fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/")
