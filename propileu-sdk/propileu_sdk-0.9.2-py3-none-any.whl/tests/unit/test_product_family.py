import json
from unittest import TestCase

import requests_mock

from propileu_sdk.config import HOST
from propileu_sdk.config import HOST_AUTH
from propileu_sdk.entities.base_manager import _authentication_logic
from propileu_sdk.sdk import ProductFamily


class ProductFamilyTest(TestCase):
    def setUp(self) -> None:
        _authentication_logic.token = None

    def test_get_a_product_family(self):
        product_family_mock = {
            "id": "4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3",
            "name": "Cano",
            "conversion_factor": "1.2000",
            "industry_id": "1c5ae68e-fbad-4470-8434-78a240bd8a4b",
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}productfamily/4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3/", json=product_family_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = ProductFamily()
            product_family = model.objects.get("4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3")

            self.assertEqual(product_family.id, "4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3")
            self.assertEqual(product_family.name, "Cano")
            self.assertEqual(product_family.industry_id, "1c5ae68e-fbad-4470-8434-78a240bd8a4b")

    def test_get_not_found_family(self):
        with requests_mock.Mocker() as m:
            m.get(f"{HOST}productfamily/4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3/", status_code=404)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            model = ProductFamily()
            model_rslt = model.objects.get("4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3")

            self.assertIsNone(model_rslt)

    def test_filter_products_family(self):
        json_mock = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3",
                    "name": "Cano",
                    "conversion_factor": "1.2000",
                    "industry_id": "1c5ae68e-fbad-4470-8434-78a240bd8a4b",
                },
                {
                    "id": "aac11161-b2fb-4075-bc63-14bebd3b06b2",
                    "name": "Cimento",
                    "conversion_factor": "1.2000",
                    "industry_id": "6074f0ca-42ae-4c1c-9a43-c1564831616a",
                },
            ],
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}productfamily/?id=&name=Cano&industry_id=", json=json_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = ProductFamily()
            model_rslt = model.objects.filter(name="Cano")

            self.assertEqual(model_rslt[0].id, "4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3")
            self.assertEqual(model_rslt[0].name, "Cano")
            self.assertEqual(model_rslt[0].conversion_factor, "1.2000")
            self.assertEqual(model_rslt[0].industry_id, "1c5ae68e-fbad-4470-8434-78a240bd8a4b")

            self.assertEqual(model_rslt[1].id, "aac11161-b2fb-4075-bc63-14bebd3b06b2")
            self.assertEqual(model_rslt[1].name, "Cimento")
            self.assertEqual(model_rslt[1].conversion_factor, "1.2000")
            self.assertEqual(model_rslt[1].industry_id, "6074f0ca-42ae-4c1c-9a43-c1564831616a")

            self.assertEqual(len(model_rslt), 2)

    def test_update_products_family(self):
        family_data = {
            "id": "update123",
            "name": "sku123",
            "conversion_factor": 1.5,
            "industry_id": "b27c0c82-59b4-483f-a598-fc8b75e094eb",
        }

        expected_family_body = {
            "id": "update123",
            "name": "sku123",
            "conversion_factor": 1.5,
            "industry_id": "b27c0c82-59b4-483f-a598-fc8b75e094eb",
        }

        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.put(f"{HOST}productfamily/update123/", json={"id": "uuid-put"})

            family = ProductFamily(**family_data)

            model = ProductFamily()
            model.objects.update(product_family=family)

            self.assertEqual(m.request_history[1].method, "PUT")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_family_body)

    def test_create_products(self):
        expected_product_body = {
            "name": "sku123",
            "conversion_factor": 1.5,
            "industry_id": "b27c0c82-59b4-483f-a598-fc8b75e094eb",
        }

        with requests_mock.Mocker() as m:
            m.post(f"{HOST}api-token-auth/", json={"token": "token123"})
            m.post(f"{HOST}productfamily/", status_code=201, json={"id": "uuid-post"})

            model = ProductFamily()
            model.objects.create(
                name="sku123", conversion_factor=1.5, industry_id="b27c0c82-59b4-483f-a598-fc8b75e094eb"
            )

            self.assertTrue(m.called)
            self.assertEqual(m.call_count, 2)
            self.assertEqual(m.request_history[1].method, "POST")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_product_body)

    def test_delete_products_family(self):
        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = ProductFamily()

            with self.assertRaises(NotImplementedError):
                model.objects.delete()
