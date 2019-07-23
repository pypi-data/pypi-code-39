import json
from unittest import TestCase

import requests_mock

from propileu_sdk.config import HOST
from propileu_sdk.config import HOST_AUTH
from propileu_sdk.entities.base_manager import _authentication_logic
from propileu_sdk.sdk import Industry


class IndustryTest(TestCase):
    def setUp(self) -> None:
        _authentication_logic.token = None

    def test_get_a_industry(self):
        industry_mock = {"id": "e507cb7c-abdc-4402-b9a6-b24c883e0733", "name": "JSM"}

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}industry/e507cb7c-abdc-4402-b9a6-b24c883e0733/", json=industry_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Industry()
            industry = model.objects.get("e507cb7c-abdc-4402-b9a6-b24c883e0733")

            self.assertEqual(industry.id, "e507cb7c-abdc-4402-b9a6-b24c883e0733")
            self.assertEqual(industry.name, "JSM")

    def test_get_not_found_industry(self):
        with requests_mock.Mocker() as m:
            m.get(f"{HOST}industry/4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3/", status_code=404)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            model = Industry()
            model_rslt = model.objects.get("4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3")

            self.assertIsNone(model_rslt)

    def test_filter_products_industry(self):
        json_mock = {
            "count": 8,
            "next": None,
            "previous": None,
            "results": [
                {"id": "e507cb7c-abdc-4402-b9a6-b24c883e0733", "name": "JSM"},
                {"id": "158cf2e5-e7d4-43c2-8f6e-3de3baf6806f", "name": "Stam"},
                {"id": "b7fe9637-6931-4b98-bdca-05739c50544a", "name": "Gerdau"},
            ],
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}industry/?name=Cano", json=json_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Industry()
            model_rslt = model.objects.filter(name="Cano")

            self.assertEqual(model_rslt[0].id, "e507cb7c-abdc-4402-b9a6-b24c883e0733")
            self.assertEqual(model_rslt[0].name, "JSM")

            self.assertEqual(model_rslt[1].id, "158cf2e5-e7d4-43c2-8f6e-3de3baf6806f")
            self.assertEqual(model_rslt[1].name, "Stam")

            self.assertEqual(len(model_rslt), 3)

    def test_update_industry(self):
        industry_data = {"id": "b7fe9637-6931-4b98-bdca-05739c50544a", "name": "Gerdau"}
        expected_industry_body = {"id": "b7fe9637-6931-4b98-bdca-05739c50544a", "name": "Gerdau"}

        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.put(f"{HOST}industry/b7fe9637-6931-4b98-bdca-05739c50544a/", json={"id": "uuid-put"})

            industry = Industry(**industry_data)

            model = Industry()
            model.objects.update(industry=industry)

            self.assertEqual(m.request_history[1].method, "PUT")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_industry_body)

    def test_create_products(self):
        expected_product_body = {"name": "JSM"}

        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.post(f"{HOST}industry/", status_code=201, json={"id": "uuid-post"})

            model = Industry()
            model.objects.create(name="JSM")

            self.assertTrue(m.called)
            self.assertEqual(m.call_count, 2)
            self.assertEqual(m.request_history[1].method, "POST")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_product_body)

    def test_delete_industry(self):
        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Industry()

            with self.assertRaises(NotImplementedError):
                model.objects.delete()
