import json

import pytest
from pytest import fixture
from requests_mock import Mocker

from propileu_sdk.config import HOST
from propileu_sdk.config import HOST_AUTH
from propileu_sdk.entities.base_manager import _authentication_logic
from propileu_sdk.entities.employee_retail_store import EmployeeRetailStore


@fixture
def prepare_authentication(requests_mock: Mocker):
    requests_mock.get(
        f"{HOST}fakes/c1d52c4a-7bd8-468f-b950-35eb4472aac9/",
        request_headers={"Authorization": "Token fake-token"},
        status_code=200,
        json={},
    )
    requests_mock.post(f"{HOST_AUTH}", json={"token": "fake-token"})

    yield requests_mock

    _authentication_logic.token = None


def test_should_get_an_employee_retail_store(prepare_authentication, requests_mock: Mocker):
    fake_employee_retail_store = {
        "id": "76f32ea8-fcea-4c81-824b-c0b47acb9d1d",
        "industry_id": "1b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "customer_id": "2b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "employee_id": "3b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "sales_office_id": "4b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "coordinator_id": "5b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "region_id": "6b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "direct": True,
    }

    requests_mock.get(
        f"{HOST}retailstoreemployee/76f32ea8-fcea-4c81-824b-c0b47acb9d1d/", json=fake_employee_retail_store
    )

    employee_retail_store_api = EmployeeRetailStore()
    retrieved_employee_retail_store = employee_retail_store_api.objects.get("76f32ea8-fcea-4c81-824b-c0b47acb9d1d")

    assert retrieved_employee_retail_store.id == "76f32ea8-fcea-4c81-824b-c0b47acb9d1d"
    assert retrieved_employee_retail_store.industry_id == "1b4172cc-c096-4ceb-9a52-3115c3abbea3"
    assert retrieved_employee_retail_store.customer_id == "2b4172cc-c096-4ceb-9a52-3115c3abbea3"
    assert retrieved_employee_retail_store.employee_id == "3b4172cc-c096-4ceb-9a52-3115c3abbea3"
    assert retrieved_employee_retail_store.sales_office_id == "4b4172cc-c096-4ceb-9a52-3115c3abbea3"
    assert retrieved_employee_retail_store.coordinator_id == "5b4172cc-c096-4ceb-9a52-3115c3abbea3"
    assert retrieved_employee_retail_store.region_id == "6b4172cc-c096-4ceb-9a52-3115c3abbea3"
    assert retrieved_employee_retail_store.direct


def test_should_return_none_if_employee_retail_store_not_found(prepare_authentication, requests_mock: Mocker):
    requests_mock.get(f"{HOST}retailstoreemployee/76f32ea8-fcea-4c81-824b-c0b47acb9d1d/", status_code=404)

    employee_retail_store_api = EmployeeRetailStore()
    retrieved_employee_retail_store = employee_retail_store_api.objects.get("76f32ea8-fcea-4c81-824b-c0b47acb9d1d")

    assert retrieved_employee_retail_store is None


def test_should_filter_employee_retail_store(prepare_authentication, requests_mock: Mocker):
    fake_drf_response = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": "76f32ea8-fcea-4c81-824b-c0b47acb9d1d",
                "industry_id": "1b4172cc-c096-4ceb-9a52-3115c3abbea3",
                "customer_id": "2b4172cc-c096-4ceb-9a52-3115c3abbea3",
                "employee_id": "3b4172cc-c096-4ceb-9a52-3115c3abbea3",
                "sales_office_id": "4b4172cc-c096-4ceb-9a52-3115c3abbea3",
                "coordinator_id": "5b4172cc-c096-4ceb-9a52-3115c3abbea3",
                "region_id": "6b4172cc-c096-4ceb-9a52-3115c3abbea3",
                "direct": True,
            }
        ],
    }

    requests_mock.get(
        f"{HOST}retailstoreemployee/?industry_id=1b4172cc-c096-4ceb-9a52-3115c3abbea3", json=fake_drf_response
    )

    employee_retail_store_api = EmployeeRetailStore()
    filtered_employee_retail_store = employee_retail_store_api.objects.filter(
        industry_id="1b4172cc-c096-4ceb-9a52-3115c3abbea3"
    )

    assert filtered_employee_retail_store[0].id == "76f32ea8-fcea-4c81-824b-c0b47acb9d1d"
    assert filtered_employee_retail_store[0].industry_id == "1b4172cc-c096-4ceb-9a52-3115c3abbea3"
    assert filtered_employee_retail_store[0].customer_id == "2b4172cc-c096-4ceb-9a52-3115c3abbea3"
    assert filtered_employee_retail_store[0].employee_id == "3b4172cc-c096-4ceb-9a52-3115c3abbea3"
    assert filtered_employee_retail_store[0].sales_office_id == "4b4172cc-c096-4ceb-9a52-3115c3abbea3"
    assert filtered_employee_retail_store[0].coordinator_id == "5b4172cc-c096-4ceb-9a52-3115c3abbea3"
    assert filtered_employee_retail_store[0].region_id == "6b4172cc-c096-4ceb-9a52-3115c3abbea3"
    assert filtered_employee_retail_store[0].direct


def test_should_update_employee_retail_store(prepare_authentication, requests_mock: Mocker):
    expected_employee_retail_store = {
        "id": "76f32ea8-fcea-4c81-824b-c0b47acb9d1d",
        "industry_id": "1b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "customer_id": "2b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "employee_id": "3b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "sales_office_id": "4b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "coordinator_id": "5b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "region_id": "6b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "direct": False,
    }

    requests_mock.put(
        f"{HOST}retailstoreemployee/76f32ea8-fcea-4c81-824b-c0b47acb9d1d/", json={"fake-key": "fake-value"}
    )

    employee_retail_store = EmployeeRetailStore(
        id="76f32ea8-fcea-4c81-824b-c0b47acb9d1d",
        industry_id="1b4172cc-c096-4ceb-9a52-3115c3abbea3",
        customer_id="2b4172cc-c096-4ceb-9a52-3115c3abbea3",
        employee_id="3b4172cc-c096-4ceb-9a52-3115c3abbea3",
        sales_office_id="4b4172cc-c096-4ceb-9a52-3115c3abbea3",
        coordinator_id="5b4172cc-c096-4ceb-9a52-3115c3abbea3",
        region_id="6b4172cc-c096-4ceb-9a52-3115c3abbea3",
        direct=False,
    )

    employee_retail_store_api = EmployeeRetailStore()
    updated_employee_retail_store = employee_retail_store_api.objects.update(employee_retail_store)

    assert updated_employee_retail_store.get("fake-key") == "fake-value"
    assert requests_mock.request_history[1].method == "PUT"
    assert json.loads(requests_mock.request_history[1].body) == expected_employee_retail_store


def test_should_create_employee_retail_store(prepare_authentication, requests_mock: Mocker):
    expected_employee_retail_store = {
        "industry_id": "1b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "customer_id": "2b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "employee_id": "3b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "sales_office_id": "4b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "coordinator_id": "5b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "region_id": "6b4172cc-c096-4ceb-9a52-3115c3abbea3",
        "direct": False,
    }

    requests_mock.post(f"{HOST}retailstoreemployee/", status_code=201, json={"fake-key": "fake-value"})

    employee_retail_store_api = EmployeeRetailStore()
    updated_employee_retail_store = employee_retail_store_api.objects.create(
        industry_id="1b4172cc-c096-4ceb-9a52-3115c3abbea3",
        customer_id="2b4172cc-c096-4ceb-9a52-3115c3abbea3",
        employee_id="3b4172cc-c096-4ceb-9a52-3115c3abbea3",
        sales_office_id="4b4172cc-c096-4ceb-9a52-3115c3abbea3",
        coordinator_id="5b4172cc-c096-4ceb-9a52-3115c3abbea3",
        region_id="6b4172cc-c096-4ceb-9a52-3115c3abbea3",
        direct=False,
    )

    assert updated_employee_retail_store.get("fake-key") == "fake-value"
    assert requests_mock.request_history[1].method == "POST"
    assert json.loads(requests_mock.request_history[1].body) == expected_employee_retail_store


def test_should_delete_employee_retail_store():
    employee_retail_store_api = EmployeeRetailStore()

    with pytest.raises(NotImplementedError):
        employee_retail_store_api.objects.delete("76f32ea8-fcea-4c81-824b-c0b47acb9d1d")
