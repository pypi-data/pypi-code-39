import typing
from time import sleep
from time import time

import pytest
import requests
from pytest_docker_compose import NetworkInfo

from propileu_sdk.entities.billing import BillingItens
from propileu_sdk.sdk import Billing
from tests.resources.support import is_valid_uuid

pytest_plugins = ["docker_compose"]


@pytest.fixture
def billing_api(docker_network_info: typing.Dict[str, typing.List[NetworkInfo]],) -> Billing:
    service = docker_network_info["resources_app_1"][0]

    # Wait for the HTTP service to be ready.
    start = time()
    timeout = 5
    for name, network_info in docker_network_info.items():
        while True:
            if time() - start >= timeout:
                raise RuntimeError(f"Unable to start all container services")
            try:

                response = requests.get(f"http://{service.hostname}:{service.host_port}/healthcheck/")
                if response.status_code == 200:
                    break
            except (ConnectionError, KeyError):
                pass
            sleep(5)

    return Billing()


@pytest.mark.skip(reason="We must solve private registry issue")
def test_should_retrieve_billing():
    billing = Billing().objects.get("abada5c0-6479-4fc1-b93d-b24d79b8d6ee")

    assert billing.id == "abada5c0-6479-4fc1-b93d-b24d79b8d6ee"
    assert billing.value == "200.1000"


@pytest.mark.skip(reason="We must solve private registry issue")
def test_should_filter_billings():
    billings = Billing().objects.filter(billing_type="type_1")

    assert type(billings) is list
    assert len(billings) == 1
    assert billings[0].billing_date == "2019-03-22"
    assert billings[0].billing_type == "type_1"
    assert billings[0].erp_code == "123"
    assert billings[0].industry_id == "bfd57441-06cd-4d67-ae59-6d0bef35418d"
    assert billings[0].store_issuer_id == "e1d85ef0-b305-4223-baa9-355b2359b46c"
    assert billings[0].store_receiver_id == "e1d85ef0-b305-4223-baa9-355b2359b46c"
    assert type(billings[0].billing_item) is list
    assert len(billings[0].billing_item) == 1
    assert billings[0].billing_item[0].product_id == "2e75354f-5114-42fd-acbc-31bb7eedb1ab"
    assert billings[0].billing_item[0].sku == "sku1"
    assert billings[0].billing_item[0].units == "1.0000"
    assert billings[0].billing_item[0].value == "200.1000"


@pytest.mark.skip(reason="We must solve private registry issue")
def test_should_create_billing():
    billing = {
        "billing_date": "2019-02-20",
        "industry_id": "bfd57441-06cd-4d67-ae59-6d0bef35418d",
        "value": "200.1000",
        "store_issuer_id": "e1d85ef0-b305-4223-baa9-355b2359b46c",
        "store_receiver_id": None,
        "erp_code": "123",
        "billing_type": "C",
        "employee_code": None,
        "direct": True,
        "billing_item": [
            BillingItens(
                value="200.1000",
                units="1.0000",
                mass="1.0000",
                bulk_type="caixa",
                product_id="2e75354f-5114-42fd-acbc-31bb7eedb1ab",
                sku="sku1",
            )
        ],
    }
    created_billing = Billing().objects.create(**billing)

    assert type(created_billing["id"]) is str
    assert is_valid_uuid(created_billing["id"])
    assert created_billing["billing_date"] == "2019-02-20"
    assert created_billing["value"] == "200.1000"
    assert created_billing["direct"] == True
    assert len(created_billing["billing_item"]) == 1
    assert is_valid_uuid(created_billing["billing_item"][0]["id"])
    assert created_billing["billing_item"][0]["product_id"] == "2e75354f-5114-42fd-acbc-31bb7eedb1ab"


@pytest.mark.skip(reason="We must solve private registry issue")
def test_should_update_billing():
    billing_to_be_updated = Billing().objects.get("fe519f92-4ad7-42a1-aa6b-d4a15d3f9ed9")
    billing_to_be_updated.value = 560.1000

    updated_billing = Billing().objects.update(billing_to_be_updated)

    assert updated_billing is not None
    assert float(updated_billing["value"]) == billing_to_be_updated.value
    assert len(updated_billing["billing_item"]) == 1
    assert is_valid_uuid(updated_billing["billing_item"][0]["id"])
