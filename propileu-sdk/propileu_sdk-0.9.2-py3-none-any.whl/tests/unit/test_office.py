import json
from unittest import TestCase

import requests_mock

from propileu_sdk.config import HOST
from propileu_sdk.config import HOST_AUTH
from propileu_sdk.entities.base_manager import _authentication_logic
from propileu_sdk.sdk import Office


class OfficeTest(TestCase):
    def setUp(self) -> None:
        _authentication_logic.token = None

    def test_get_a_office(self):
        office_mock = {
            "id": "e507cb7c-abdc-4402-b9a6-b24c883e0733",
            "name": "Office 1",
            "industry_id": "b78b8ac3-174c-419d-ae95-8b6e215d3ff4",
            "erp_code": "123",
            "direct": True,
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}office/e507cb7c-abdc-4402-b9a6-b24c883e0733/", json=office_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Office()
            office = model.objects.get("e507cb7c-abdc-4402-b9a6-b24c883e0733")

            self.assertEqual(office.id, "e507cb7c-abdc-4402-b9a6-b24c883e0733")
            self.assertEqual(office.name, "Office 1")
            self.assertEqual(office.industry_id, "b78b8ac3-174c-419d-ae95-8b6e215d3ff4")
            self.assertEqual(office.erp_code, "123")
            self.assertTrue(office.direct)

    def test_get_not_found_office(self):
        with requests_mock.Mocker() as m:
            m.get(f"{HOST}office/4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3/", status_code=404)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            model = Office()
            model_rslt = model.objects.get("4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3")

            self.assertIsNone(model_rslt)

    def test_filter_products_office(self):
        json_mock = {
            "count": 8,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "e507cb7c-abdc-4402-b9a6-b24c883e0733",
                    "name": "Office 1",
                    "industry_id": "b78b8ac3-174c-419d-ae95-8b6e215d3ff4",
                    "erp_code": "123",
                    "direct": True,
                },
                {
                    "id": "158cf2e5-e7d4-43c2-8f6e-3de3baf6806f",
                    "name": "Stam",
                    "industry_id": "b78b8ac3-174c-419d-aa95-8b6e215d3ff4",
                    "erp_code": "456",
                },
                {
                    "id": "b7fe9637-6931-4b98-bdca-05739c50544a",
                    "name": "Gerdau",
                    "industry_id": "b78b8ac3-174c-419d-ae95-8b6e215d3ff4",
                    "erp_code": "789",
                },
            ],
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}office/?name=Cano", json=json_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Office()
            model_rslt = model.objects.filter(name="Cano")

            self.assertEqual(model_rslt[0].id, "e507cb7c-abdc-4402-b9a6-b24c883e0733")
            self.assertEqual(model_rslt[0].name, "Office 1")
            self.assertEqual(model_rslt[0].industry_id, "b78b8ac3-174c-419d-ae95-8b6e215d3ff4")
            self.assertEqual(model_rslt[0].erp_code, "123")
            self.assertTrue(model_rslt[0].direct)

            self.assertEqual(model_rslt[1].id, "158cf2e5-e7d4-43c2-8f6e-3de3baf6806f")
            self.assertEqual(model_rslt[1].name, "Stam")
            self.assertEqual(model_rslt[1].industry_id, "b78b8ac3-174c-419d-aa95-8b6e215d3ff4")
            self.assertEqual(model_rslt[1].erp_code, "456")
            self.assertFalse(model_rslt[1].direct)

            self.assertEqual(len(model_rslt), 3)

    def test_update_office(self):
        office_data = {
            "id": "b7fe9637-6931-4b98-bdca-05739c50544a",
            "name": "Gerdau",
            "industry_id": "b78b8ac3-174c-419d-ae95-8b6e215d3ff4",
            "erp_code": "123",
            "direct": True,
        }

        expected_office_body = {
            "id": "b7fe9637-6931-4b98-bdca-05739c50544a",
            "name": "Gerdau",
            "industry_id": "b78b8ac3-174c-419d-ae95-8b6e215d3ff4",
            "erp_code": "123",
            "direct": True,
        }

        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.put(f"{HOST}office/b7fe9637-6931-4b98-bdca-05739c50544a/", json={"id": "uuid-put"})

            office = Office(**office_data)

            model = Office()
            model.objects.update(office=office)

            self.assertEqual(m.request_history[1].method, "PUT")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_office_body)

    def test_create_products(self):
        expected_product_body = {
            "name": "Office 1",
            "industry_id": "b78b8ac3-174c-419d-ae95-8b6e215d3ff4",
            "erp_code": "123",
            "direct": True,
        }

        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.post(f"{HOST}office/", status_code=201, json={"id": "uuid-post"})

            model = Office()
            model.objects.create(
                name="Office 1", industry_id="b78b8ac3-174c-419d-ae95-8b6e215d3ff4", erp_code="123", direct=True
            )

            self.assertTrue(m.called)
            self.assertEqual(m.call_count, 2)
            self.assertEqual(m.request_history[1].method, "POST")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_product_body)

    def test_delete_office(self):
        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Office()

            with self.assertRaises(NotImplementedError):
                model.objects.delete()
