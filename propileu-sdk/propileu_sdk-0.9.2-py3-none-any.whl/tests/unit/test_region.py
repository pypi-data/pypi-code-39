import json
from unittest import TestCase

import requests_mock

from propileu_sdk.config import HOST
from propileu_sdk.config import HOST_AUTH
from propileu_sdk.entities.base_manager import _authentication_logic
from propileu_sdk.sdk import Regions


class RegionsTest(TestCase):
    def setUp(self) -> None:
        _authentication_logic.token = None

    def test_get_a_region(self):
        region_mock = {
            "id": "426e0747-a3ed-460b-96d1-722248c17e08",
            "name": "Região 2",
            "industry_id": "1bde6d8d-0acd-4a54-a1f1-9551ac0533aa",
            "erp_code": "345",
            "direct": True,
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}regions/426e0747-a3ed-460b-96d1-722248c17e08/", json=region_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Regions()
            region = model.objects.get("426e0747-a3ed-460b-96d1-722248c17e08")

            self.assertEqual(region.id, "426e0747-a3ed-460b-96d1-722248c17e08")
            self.assertEqual(region.name, "Região 2")
            self.assertEqual(region.industry_id, "1bde6d8d-0acd-4a54-a1f1-9551ac0533aa")
            self.assertEqual(region.erp_code, "345")
            self.assertTrue(region.direct)

    def test_get_not_found_regions(self):
        with requests_mock.Mocker() as m:
            m.get(f"{HOST}regions/4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3/", status_code=404)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            model = Regions()
            model_rslt = model.objects.get("4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3")

            self.assertIsNone(model_rslt)

    def test_filter_products_regions(self):
        json_mock = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "426e0747-a3ed-460b-96d1-722248c17e08",
                    "name": "Região 2",
                    "industry_id": "1bde6d8d-0acd-4a54-a1f1-9551ac0533aa",
                    "erp_code": "345",
                    "direct": True,
                },
                {
                    "id": "0ec37ce9-1134-4fb3-ba68-ed24dc99a00f",
                    "name": "Sul",
                    "industry_id": "269aee3a-7fa0-43b4-89c0-a30aac90967a",
                    "erp_code": "765",
                },
            ],
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}regions/?id=&name=Cano&industry_id=", json=json_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Regions()
            model_rslt = model.objects.filter(name="Cano")

            self.assertEqual(model_rslt[0].id, "426e0747-a3ed-460b-96d1-722248c17e08")
            self.assertEqual(model_rslt[0].name, "Região 2")
            self.assertEqual(model_rslt[0].erp_code, "345")
            self.assertEqual(model_rslt[0].industry_id, "1bde6d8d-0acd-4a54-a1f1-9551ac0533aa")
            self.assertTrue(model_rslt[0].direct)

            self.assertEqual(model_rslt[1].id, "0ec37ce9-1134-4fb3-ba68-ed24dc99a00f")
            self.assertEqual(model_rslt[1].name, "Sul")
            self.assertEqual(model_rslt[1].erp_code, "765")
            self.assertEqual(model_rslt[1].industry_id, "269aee3a-7fa0-43b4-89c0-a30aac90967a")

            self.assertEqual(len(model_rslt), 2)

    def test_update_regions(self):
        regions_data = {
            "id": "426e0747-a3ed-460b-96d1-722248c17e08",
            "name": "Região 2",
            "industry_id": "1bde6d8d-0acd-4a54-a1f1-9551ac0533aa",
            "erp_code": "345",
            "direct": True,
        }

        expected_regions_body = {
            "id": "426e0747-a3ed-460b-96d1-722248c17e08",
            "name": "Região 2",
            "industry_id": "1bde6d8d-0acd-4a54-a1f1-9551ac0533aa",
            "erp_code": "345",
            "direct": True,
        }

        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.put(f"{HOST}regions/426e0747-a3ed-460b-96d1-722248c17e08/", json={"id": "uuid-put"})

            regions = Regions(**regions_data)

            model = Regions()
            model.objects.update(regions=regions)

            self.assertEqual(m.request_history[1].method, "PUT")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_regions_body)

    def test_create_products(self):
        expected_product_body = {
            "name": "Região 2",
            "industry_id": "1bde6d8d-0acd-4a54-a1f1-9551ac0533aa",
            "erp_code": "345",
            "direct": True,
        }

        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.post(f"{HOST}regions/", status_code=201, json={"id": "uuid-post"})

            model = Regions()
            model.objects.create(
                name="Região 2", erp_code="345", industry_id="1bde6d8d-0acd-4a54-a1f1-9551ac0533aa", direct=True
            )

            self.assertTrue(m.called)
            self.assertEqual(m.call_count, 2)
            self.assertEqual(m.request_history[1].method, "POST")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_product_body)

    def test_delete_region(self):
        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Regions()

            with self.assertRaises(NotImplementedError):
                model.objects.delete()
