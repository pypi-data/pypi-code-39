import json
from unittest import TestCase

import requests_mock

from propileu_sdk.config import HOST
from propileu_sdk.config import HOST_AUTH
from propileu_sdk.entities.base_manager import _authentication_logic
from propileu_sdk.sdk import Billing
from propileu_sdk.sdk import BillingItens


class BillingTest(TestCase):
    def setUp(self) -> None:
        _authentication_logic.token = None

    def test_get_a_billing(self):
        billing_mock = {
            "id": "c1d52c4a-7bd8-468f-b950-35eb4472aac9",
            "billing_date": "2019-02-20",
            "industry_id": "8cee454a-bc0f-412c-825c-a7ef9d81698c",
            "value": "200.1000",
            "store_issuer_id": "24a41eb6-c621-4afe-b490-8eb4580b601b",
            "store_receiver_id": "24a41eb6-c621-4afe-b490-8eb4580b601b",
            "erp_code": "123",
            "billing_type": "type_1",
            "employee_code": "empcode",
            "direct": True,
            "billing_item": [
                {
                    "value": "200.1000",
                    "units": "1.0000",
                    "mass": "1.0000",
                    "bulk_type": "caixa",
                    "product_id": "ac236cb1-6bbe-4c2c-81ba-caa5ea82dce7",
                    "sku": "sku1",
                }
            ],
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}billing/c1d52c4a-7bd8-468f-b950-35eb4472aac9/", json=billing_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Billing()
            model_result = model.objects.get("c1d52c4a-7bd8-468f-b950-35eb4472aac9")

            self.assertEqual(model_result.id, "c1d52c4a-7bd8-468f-b950-35eb4472aac9")
            self.assertEqual(model_result.industry_id, "8cee454a-bc0f-412c-825c-a7ef9d81698c")
            self.assertEqual(model_result.billing_date, "2019-02-20")
            self.assertEqual(model_result.store_issuer_id, "24a41eb6-c621-4afe-b490-8eb4580b601b")
            self.assertEqual(model_result.store_receiver_id, "24a41eb6-c621-4afe-b490-8eb4580b601b")
            self.assertEqual(model_result.billing_type, "type_1")
            self.assertEqual(model_result.erp_code, "123")
            self.assertEqual(model_result.employee_code, "empcode")
            self.assertIsInstance(model_result.billing_item[0], BillingItens)
            self.assertEqual(model_result.billing_item[0].value, "200.1000")
            self.assertEqual(model_result.billing_item[0].units, "1.0000")
            self.assertEqual(model_result.billing_item[0].mass, "1.0000")
            self.assertEqual(model_result.billing_item[0].sku, "sku1")
            self.assertEqual(model_result.billing_item[0].bulk_type, "caixa")
            self.assertEqual(model_result.billing_item[0].product_id, "ac236cb1-6bbe-4c2c-81ba-caa5ea82dce7")
            self.assertEqual(len(model_result.billing_item), 1)
            self.assertTrue(model_result.direct)

    def test_get_not_found_billing(self):
        with requests_mock.Mocker() as m:
            m.get(f"{HOST}billing/4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3/", status_code=404)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            model = Billing()
            model_rslt = model.objects.get("4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3")

            self.assertIsNone(model_rslt)

    def test_filter_billing(self):
        json_mock = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "12dd11e5-29c0-4ff4-af43-fd2cb0b51324",
                    "billing_date": "2019-02-20",
                    "industry_id": "1011de4f-4ee5-42c7-8f10-5f059d42dff5",
                    "value": "200.1000",
                    "store_issuer_id": "a3a5cbbd-ad32-4bab-9be7-50a86cd5f36e",
                    "store_receiver_id": "a3a5cbbd-ad32-4bab-9be7-50a86cd5f36e",
                    "erp_code": "123",
                    "billing_type": "type_1",
                    "employee_code": "empcode",
                    "direct": True,
                    "billing_item": [
                        {
                            "id": "12dd11e5-29c0-4ff4-af43-fd2cb0b51324",
                            "value": "200.1000",
                            "units": "1.0000",
                            "mass": "1.0000",
                            "bulk_type": "caixa",
                            "product_id": "fbcd81b5-f576-4f6c-b9c9-4b851c0c892b",
                            "sku": "sku1",
                        }
                    ],
                }
            ],
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}billing/?industry_id=1011de4f-4ee5-42c7-8f10-5f059d42dff5", json=json_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Billing()
            model_result = model.objects.filter(industry_id="1011de4f-4ee5-42c7-8f10-5f059d42dff5")

            self.assertEqual(model_result[0].id, "12dd11e5-29c0-4ff4-af43-fd2cb0b51324")
            self.assertEqual(model_result[0].industry_id, "1011de4f-4ee5-42c7-8f10-5f059d42dff5")
            self.assertEqual(model_result[0].billing_date, "2019-02-20")
            self.assertEqual(model_result[0].billing_type, "type_1")
            self.assertEqual(model_result[0].employee_code, "empcode")
            self.assertEqual(model_result[0].store_issuer_id, "a3a5cbbd-ad32-4bab-9be7-50a86cd5f36e")
            self.assertEqual(model_result[0].store_receiver_id, "a3a5cbbd-ad32-4bab-9be7-50a86cd5f36e")
            self.assertEqual(model_result[0].erp_code, "123")
            self.assertIsInstance(model_result[0].billing_item[0], BillingItens)
            self.assertEqual(model_result[0].billing_item[0].value, "200.1000")
            self.assertEqual(model_result[0].billing_item[0].units, "1.0000")
            self.assertEqual(model_result[0].billing_item[0].mass, "1.0000")
            self.assertEqual(model_result[0].billing_item[0].sku, "sku1")
            self.assertEqual(model_result[0].billing_item[0].bulk_type, "caixa")
            self.assertEqual(model_result[0].billing_item[0].product_id, "fbcd81b5-f576-4f6c-b9c9-4b851c0c892b")
            self.assertEqual(len(model_result[0].billing_item), 1)
            self.assertTrue(model_result[0].direct)
            self.assertEqual(len(model_result), 1)

    def test_update_billing(self):

        expected_billing_body = {
            "id": "12dd11e5-29c0-4ff4-af43-fd2cb0b51324",
            "billing_date": "2019-02-20",
            "industry_id": "1011de4f-4ee5-42c7-8f10-5f059d42dff5",
            "value": "200.1000",
            "store_issuer_id": "a3a5cbbd-ad32-4bab-9be7-50a86cd5f36e",
            "store_receiver_id": "a3a5cbbd-ad32-4bab-9be7-50a86cd5f36e",
            "erp_code": "123",
            "billing_type": "type_1",
            "employee_code": "empcode",
            "direct": True,
            "billing_item": [
                {
                    "id": "fbcd81b5-f576-4f6c-b9c9-4b851c0c892b",
                    "value": "200.1000",
                    "units": "1.0000",
                    "mass": "1.0000",
                    "bulk_type": "caixa",
                    "product_id": "fbcd81b5-f576-4f6c-b9c9-4b851c0c892b",
                    "sku": "sku1",
                }
            ],
        }
        billing = Billing(
            id="12dd11e5-29c0-4ff4-af43-fd2cb0b51324",
            billing_date="2019-02-20",
            industry_id="1011de4f-4ee5-42c7-8f10-5f059d42dff5",
            value="200.1000",
            store_issuer_id="a3a5cbbd-ad32-4bab-9be7-50a86cd5f36e",
            store_receiver_id="a3a5cbbd-ad32-4bab-9be7-50a86cd5f36e",
            erp_code="123",
            billing_type="type_1",
            employee_code="empcode",
            direct=True,
        )

        billing.billing_item = [
            BillingItens(
                id="fbcd81b5-f576-4f6c-b9c9-4b851c0c892b",
                value="200.1000",
                units="1.0000",
                mass="1.0000",
                bulk_type="caixa",
                product_id="fbcd81b5-f576-4f6c-b9c9-4b851c0c892b",
                sku="sku1",
            )
        ]

        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.put(f"{HOST}billing/12dd11e5-29c0-4ff4-af43-fd2cb0b51324/", json={"id": "uuid-put"})

            model = Billing()
            model.objects.update(billing=billing)

            self.assertEqual(m.request_history[1].method, "PUT")
            self.assertEqual(json.loads(m.request_history[1].body), expected_billing_body)

    def test_create_billing(self):
        expected_billing_body = {
            "billing_date": "2019-02-20",
            "industry_id": "1011de4f-4ee5-42c7-8f10-5f059d42dff5",
            "value": "200.1000",
            "store_issuer_id": "a3a5cbbd-ad32-4bab-9be7-50a86cd5f36e",
            "store_receiver_id": "a3a5cbbd-ad32-4bab-9be7-50a86cd5f36e",
            "erp_code": "123",
            "billing_type": "type_1",
            "employee_code": "empcode",
            "direct": True,
            "billing_item": [
                {
                    "value": "200.1000",
                    "units": "1.0000",
                    "mass": "1.0000",
                    "bulk_type": "caixa",
                    "product_id": "fbcd81b5-f576-4f6c-b9c9-4b851c0c892b",
                    "sku": "sku1",
                }
            ],
        }

        item = BillingItens(
            value="200.1000",
            units="1.0000",
            mass="1.0000",
            bulk_type="caixa",
            product_id="fbcd81b5-f576-4f6c-b9c9-4b851c0c892b",
            sku="sku1",
        )

        with requests_mock.Mocker() as m:

            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.post(f"{HOST}billing/", status_code=201, json={"id": "uuid-post"})

            model = Billing()
            model.objects.create(
                billing_date="2019-02-20",
                billing_type="type_1",
                industry_id="1011de4f-4ee5-42c7-8f10-5f059d42dff5",
                value="200.1000",
                store_issuer_id="a3a5cbbd-ad32-4bab-9be7-50a86cd5f36e",
                store_receiver_id="a3a5cbbd-ad32-4bab-9be7-50a86cd5f36e",
                erp_code="123",
                billing_item=[item],
                employee_code="empcode",
                direct=True,
            )

            self.assertTrue(m.called)
            self.assertEqual(m.call_count, 2)
            self.assertEqual(m.request_history[1].method, "POST")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_billing_body)

    def test_delete_billing(self):
        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            model = Billing()
            with self.assertRaises(NotImplementedError):
                model.objects.delete()
