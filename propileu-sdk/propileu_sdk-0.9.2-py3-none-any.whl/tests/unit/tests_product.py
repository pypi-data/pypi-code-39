import json
from unittest import TestCase

import requests_mock

from propileu_sdk.config import HOST
from propileu_sdk.config import HOST_AUTH
from propileu_sdk.entities.base_manager import _authentication_logic
from propileu_sdk.sdk import Product


class ProductSKUTest(TestCase):
    def setUp(self) -> None:
        _authentication_logic.token = None

    def test_get_a_product(self):
        product_mock = {
            "id": "df77fc40-3cab-4669-a202-aeb48725bfb3",
            "sku": "abc",
            "description": "Curva 45 PBS",
            "conversion_factor": "1.5000",
            "family_id": "5df4ecc3-5048-4d87-9c9a-990d45e12ff6",
            "industry_id": "b27c0c82-59b4-483f-a598-fc8b75e094eb",
            "direct": True,
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}product/product123/", json=product_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Product()
            product_rslt = model.objects.get("product123")

            self.assertEqual(product_rslt.id, "df77fc40-3cab-4669-a202-aeb48725bfb3")
            self.assertEqual(product_rslt.sku, "abc")
            self.assertEqual(product_rslt.family_id, "5df4ecc3-5048-4d87-9c9a-990d45e12ff6")
            self.assertEqual(product_rslt.conversion_factor, "1.5000")
            self.assertEqual(product_rslt.description, "Curva 45 PBS")
            self.assertEqual(product_rslt.industry_id, "b27c0c82-59b4-483f-a598-fc8b75e094eb")
            self.assertTrue(product_rslt.direct)

    def test_get_not_found(self):
        with requests_mock.Mocker() as m:
            m.get(f"{HOST}product/product123/", status_code=404)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            model = Product()
            product_rslt = model.objects.get("product123")

            self.assertIsNone(product_rslt)

    def test_filter_products(self):
        products_mock = {
            "count": 4,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "df77fc40-3cab-4669-a202-aeb48725bfb3",
                    "sku": "abc",
                    "description": "Curva 45 PBS",
                    "conversion_factor": "1.5000",
                    "family_id": "5df4ecc3-5048-4d87-9c9a-990d45e12ff6",
                    "industry_id": "b27c0c82-59b4-483f-a598-fc8b75e094eb",
                    "direct": True,
                },
                {
                    "id": "4bf0421d-66ba-48b2-9cce-937f5264d5db",
                    "sku": "789",
                    "description": "Adaptador PBS com bolsa e rosca",
                    "conversion_factor": "1.5000",
                    "family_id": "5df4ecc3-5048-4d87-9c9a-990d45e12ff6",
                    "industry_id": "b27c0c82-59b4-483f-a598-fc8b75e094eb",
                },
                {
                    "id": "5a69724b-7138-4354-b957-a91f0ed99cae",
                    "sku": "456",
                    "description": "Cimento Cp II 50kg Cinza Nacional",
                    "conversion_factor": "1.5000",
                    "family_id": "5df4ecc3-5048-4d87-9c9a-990d45e12ff6",
                    "industry_id": "6fa1cac4-6de6-455c-b08b-d212592a8c24",
                },
                {
                    "id": "594219be-9141-488f-905a-d33a8a122277",
                    "sku": "123",
                    "description": "Cimento Cp II 25kg Cinza Nacional",
                    "conversion_factor": "1.5000",
                    "family_id": "5df4ecc3-5048-4d87-9c9a-990d45e12ff6",
                    "industry_id": "6fa1cac4-6de6-455c-b08b-d212592a8c24",
                },
            ],
        }

        with requests_mock.Mocker() as m:
            m.get(
                f"{HOST}product/?id=&sku=&family_id=5df4ecc3-5048-4d87-9c9a-990d45e12ff6&industry_id=",
                json=products_mock,
            )
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Product()
            products = model.objects.filter(family_id="5df4ecc3-5048-4d87-9c9a-990d45e12ff6")

            self.assertEqual(products[0].id, "df77fc40-3cab-4669-a202-aeb48725bfb3")
            self.assertEqual(products[0].sku, "abc")
            self.assertEqual(products[0].family_id, "5df4ecc3-5048-4d87-9c9a-990d45e12ff6")
            self.assertEqual(products[0].conversion_factor, "1.5000")
            self.assertEqual(products[0].industry_id, "b27c0c82-59b4-483f-a598-fc8b75e094eb")
            self.assertEqual(products[0].description, "Curva 45 PBS")
            self.assertTrue(products[0].direct)

            self.assertEqual(products[1].id, "4bf0421d-66ba-48b2-9cce-937f5264d5db")
            self.assertEqual(products[1].sku, "789")
            self.assertEqual(products[1].family_id, "5df4ecc3-5048-4d87-9c9a-990d45e12ff6")
            self.assertEqual(products[1].conversion_factor, "1.5000")
            self.assertEqual(products[1].industry_id, "b27c0c82-59b4-483f-a598-fc8b75e094eb")
            self.assertEqual(products[1].description, "Adaptador PBS com bolsa e rosca")

            self.assertEqual(len(products), 4)

    def test_update_products(self):
        product_data = {
            "id": "update123",
            "sku": "sku123",
            "family_id": "family123",
            "conversion_factor": 1.5,
            "description": "Curva 45 PBS",
            "industry_id": "b27c0c82-59b4-483f-a598-fc8b75e094eb",
            "direct": True,
        }

        expected_product_body = {
            "id": "update123",
            "sku": "sku123",
            "description": "Curva 45 PBS",
            "conversion_factor": 1.5,
            "family_id": "family123",
            "industry_id": "b27c0c82-59b4-483f-a598-fc8b75e094eb",
            "direct": True,
        }

        with requests_mock.Mocker() as m:

            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.put(f"{HOST}product/update123/", json={"id": "uuid-put"})

            product = Product(**product_data)

            model = Product()
            model.objects.update(product=product)

            self.assertEqual(m.request_history[1].method, "PUT")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_product_body)

    def test_create_products(self):
        expected_product_body = {
            "sku": "sku123",
            "description": "Curva 45 PBS",
            "conversion_factor": 1.5,
            "family_id": "family123",
            "industry_id": "b27c0c82-59b4-483f-a598-fc8b75e094eb",
            "direct": True,
        }

        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.post(f"{HOST}product/", status_code=201, json={})

            model = Product()
            model.objects.create(
                sku="sku123",
                family_id="family123",
                conversion_factor=1.5,
                description="Curva 45 PBS",
                industry_id="b27c0c82-59b4-483f-a598-fc8b75e094eb",
                direct=True,
            )

            self.assertTrue(m.called)
            self.assertEqual(m.call_count, 2)
            self.assertEqual(m.request_history[1].method, "POST")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_product_body)

    def test_delete_products(self):
        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Product()

            with self.assertRaises(NotImplementedError):
                model.objects.delete()
