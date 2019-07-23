import json
from unittest import TestCase

import requests_mock

from propileu_sdk.config import HOST
from propileu_sdk.config import HOST_AUTH
from propileu_sdk.entities.base_manager import _authentication_logic
from propileu_sdk.sdk import RetailStore
from propileu_sdk.sdk import RetailStoreAddress
from propileu_sdk.sdk import RetailStoreDealer
from propileu_sdk.sdk import RetailStoreDealerEmail
from propileu_sdk.sdk import RetailStoreDealerPhone
from propileu_sdk.sdk import RetailStorePhone
from propileu_sdk.sdk import RetailStoreTag


class RetailStoreTest(TestCase):
    maxDiff = None

    def setUp(self) -> None:
        _authentication_logic.token = None

    def test_get_a_retail_store(self):
        json_mock = {
            "id": "74633baa-3063-4537-9eca-71a7af212d6f",
            "social_name": "Nome social",
            "erp_code": "123",
            "business_region": "test de regiao",
            "registered_at_partner": "2019-02-20",
            "cnpj": "123456",
            "cnpj_root": "123456",
            "direct": True,
            "retail_store_tags": [{"name": "tag2"}, {"name": "tag1"}],
            "retail_store_phones": [
                {"value": "56666933854", "phone_type": 2},
                {"value": "55566999854", "phone_type": 1},
            ],
            "retail_store_address": [
                {
                    "address_type": "MAIN",
                    "city": "SÃO PAULO",
                    "state_or_province": "SP",
                    "street_with_house_number_or_name": "Rua com o número",
                    "neighborhood": "Vila Indiana",
                    "country": "Brasil",
                    "postal_code": "12344567",
                    "mesoregion": "Meso Region",
                    "microregion": "Micro Region",
                    "city_council_code": "1234",
                }
            ],
            "retail_store_dealer": [
                {
                    "dealer_email": [{"email": "email 2"}, {"email": "email 1"}],
                    "dealer_phones": [
                        {"value": "56666933854", "phone_type": 2},
                        {"value": "55566999854", "phone_type": 1},
                    ],
                }
            ],
            "industry_id": "83c81318-bd76-435f-b4b0-1c8dd1e79849",
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}retailstore/74633baa-3063-4537-9eca-71a7af212d6f/", json=json_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = RetailStore()
            model_result = model.objects.get("74633baa-3063-4537-9eca-71a7af212d6f")

            self.assertEqual(model_result.id, "74633baa-3063-4537-9eca-71a7af212d6f")
            self.assertEqual(model_result.erp_code, "123")
            self.assertEqual(model_result.social_name, "Nome social")
            self.assertEqual(model_result.industry_id, "83c81318-bd76-435f-b4b0-1c8dd1e79849")
            self.assertEqual(model_result.business_region, "test de regiao")
            self.assertEqual(model_result.registered_at_partner, "2019-02-20")
            self.assertTrue(model_result.direct)

            self.assertEqual(model_result.cnpj, "123456")
            self.assertEqual(model_result.cnpj_root, "123456")

            self.assertIsInstance(model_result.retail_store_tags[0], RetailStoreTag)
            self.assertIsInstance(model_result.retail_store_phones[0], RetailStorePhone)
            self.assertIsInstance(model_result.retail_store_address[0], RetailStoreAddress)
            self.assertIsInstance(model_result.retail_store_dealer[0], RetailStoreDealer)
            self.assertIsInstance(
                model_result.retail_store_dealer[0].retail_store_dealer_emails[0], RetailStoreDealerEmail
            )
            self.assertIsInstance(
                model_result.retail_store_dealer[0].retail_store_dealer_phones[0], RetailStoreDealerPhone
            )

            self.assertEqual(model_result.retail_store_tags[0].name, "tag2")
            self.assertEqual(model_result.retail_store_phones[0].phone_type, 2)
            self.assertEqual(model_result.retail_store_phones[0].value, "56666933854")
            self.assertEqual(model_result.retail_store_address[0].address_type, "MAIN")
            self.assertEqual(model_result.retail_store_address[0].city, "SÃO PAULO")
            self.assertEqual(model_result.retail_store_address[0].state_or_province, "SP")
            self.assertEqual(model_result.retail_store_address[0].street_with_house_number_or_name, "Rua com o número")
            self.assertEqual(model_result.retail_store_address[0].neighborhood, "Vila Indiana")
            self.assertEqual(model_result.retail_store_address[0].country, "Brasil")
            self.assertEqual(model_result.retail_store_address[0].postal_code, "12344567")
            self.assertEqual(model_result.retail_store_address[0].mesoregion, "Meso Region")
            self.assertEqual(model_result.retail_store_address[0].microregion, "Micro Region")
            self.assertEqual(model_result.retail_store_address[0].city_council_code, "1234")

            self.assertEqual(model_result.retail_store_dealer[0].retail_store_dealer_phones[0].value, "56666933854")
            self.assertEqual(model_result.retail_store_dealer[0].retail_store_dealer_phones[0].phone_type, 2)

            self.assertEqual(model_result.retail_store_dealer[0].retail_store_dealer_emails[0].email, "email 2")

            self.assertEqual(len(model_result.retail_store_tags), 2)
            self.assertEqual(len(model_result.retail_store_phones), 2)
            self.assertEqual(len(model_result.retail_store_address), 1)

            self.assertEqual(len(model_result.retail_store_dealer), 1)
            self.assertEqual(len(model_result.retail_store_dealer[0].retail_store_dealer_phones), 2)
            self.assertEqual(len(model_result.retail_store_dealer[0].retail_store_dealer_emails), 2)

    def test_get_not_found_retail_store(self):
        with requests_mock.Mocker() as m:
            m.get(f"{HOST}retailstore/4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3/", status_code=404)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            model = RetailStore()
            model_rslt = model.objects.get("4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3")

            self.assertIsNone(model_rslt)

    def test_filter_retail_store(self):
        json_mock = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "74633baa-3063-4537-9eca-71a7af212d6f",
                    "social_name": "Nome social",
                    "erp_code": "123",
                    "business_region": "test de regiao",
                    "registered_at_partner": "2019-02-20",
                    "cnpj": "123456",
                    "cnpj_root": "123456",
                    "retail_store_tags": [{"name": "tag2"}, {"name": "tag1"}],
                    "retail_store_phones": [
                        {"value": "56666933854", "phone_type": 2},
                        {"value": "55566999854", "phone_type": 1},
                    ],
                    "retail_store_address": [
                        {
                            "address_type": "MAIN",
                            "city": "SÃO PAULO",
                            "state_or_province": "SP",
                            "street_with_house_number_or_name": "Rua com o número",
                            "neighborhood": "Vila Indiana",
                            "country": "Brasil",
                            "postal_code": "12344567",
                            "mesoregion": "Meso Region",
                            "microregion": "Micro Region",
                            "city_council_code": "1234",
                        }
                    ],
                    "retail_store_dealer": [
                        {
                            "dealer_email": [{"email": "email 2"}, {"email": "email 1"}],
                            "dealer_phones": [
                                {"value": "56666933854", "phone_type": 2},
                                {"value": "55566999854", "phone_type": 1},
                            ],
                        }
                    ],
                    "industry_id": "83c81318-bd76-435f-b4b0-1c8dd1e79849",
                }
            ],
        }

        with requests_mock.Mocker() as m:
            m.get(
                f"{HOST}retailstore/?id=&social_name=Nome social&erp_code=&business_region=&registered_at_partner=&mesoregion=&microregion=&cnpj=&cnpj_root=&city_council_code=&industry_id=",
                json=json_mock,
            )
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = RetailStore()
            model_result = model.objects.filter(social_name="Nome social")

            self.assertEqual(model_result[0].id, "74633baa-3063-4537-9eca-71a7af212d6f")
            self.assertEqual(model_result[0].erp_code, "123")
            self.assertEqual(model_result[0].social_name, "Nome social")
            self.assertEqual(model_result[0].industry_id, "83c81318-bd76-435f-b4b0-1c8dd1e79849")
            self.assertEqual(model_result[0].business_region, "test de regiao")
            self.assertEqual(model_result[0].registered_at_partner, "2019-02-20")

            self.assertEqual(model_result[0].cnpj, "123456")
            self.assertEqual(model_result[0].cnpj_root, "123456")

            self.assertIsInstance(model_result[0].retail_store_tags[0], RetailStoreTag)
            self.assertIsInstance(model_result[0].retail_store_phones[0], RetailStorePhone)
            self.assertIsInstance(model_result[0].retail_store_address[0], RetailStoreAddress)
            self.assertIsInstance(model_result[0].retail_store_dealer[0], RetailStoreDealer)
            self.assertIsInstance(
                model_result[0].retail_store_dealer[0].retail_store_dealer_emails[0], RetailStoreDealerEmail
            )
            self.assertIsInstance(
                model_result[0].retail_store_dealer[0].retail_store_dealer_phones[0], RetailStoreDealerPhone
            )

            self.assertEqual(model_result[0].retail_store_tags[0].name, "tag2")
            self.assertEqual(model_result[0].retail_store_phones[0].phone_type, 2)
            self.assertEqual(model_result[0].retail_store_phones[0].value, "56666933854")
            self.assertEqual(model_result[0].retail_store_address[0].address_type, "MAIN")
            self.assertEqual(model_result[0].retail_store_address[0].city, "SÃO PAULO")
            self.assertEqual(model_result[0].retail_store_address[0].state_or_province, "SP")
            self.assertEqual(
                model_result[0].retail_store_address[0].street_with_house_number_or_name, "Rua com o número"
            )
            self.assertEqual(model_result[0].retail_store_address[0].neighborhood, "Vila Indiana")
            self.assertEqual(model_result[0].retail_store_address[0].country, "Brasil")
            self.assertEqual(model_result[0].retail_store_address[0].postal_code, "12344567")
            self.assertEqual(model_result[0].retail_store_address[0].mesoregion, "Meso Region")
            self.assertEqual(model_result[0].retail_store_address[0].microregion, "Micro Region")
            self.assertEqual(model_result[0].retail_store_address[0].city_council_code, "1234")

            self.assertEqual(model_result[0].retail_store_dealer[0].retail_store_dealer_phones[0].value, "56666933854")
            self.assertEqual(model_result[0].retail_store_dealer[0].retail_store_dealer_phones[0].phone_type, 2)

            self.assertEqual(model_result[0].retail_store_dealer[0].retail_store_dealer_emails[0].email, "email 2")

            self.assertEqual(len(model_result[0].retail_store_tags), 2)
            self.assertEqual(len(model_result[0].retail_store_phones), 2)
            self.assertEqual(len(model_result[0].retail_store_address), 1)
            self.assertEqual(len(model_result[0].retail_store_dealer), 1)
            self.assertEqual(len(model_result[0].retail_store_dealer[0].retail_store_dealer_phones), 2)
            self.assertEqual(len(model_result[0].retail_store_dealer[0].retail_store_dealer_emails), 2)

            self.assertEqual(len(model_result), 1)

    def test_update_retail_store(self):
        expected_retail_store_body = {
            "direct": False,
            "id": "74633baa-3063-4537-9eca-71a7af212d6f",
            "social_name": "Nome social",
            "erp_code": "123",
            "business_region": "test de regiao",
            "registered_at_partner": "2019-02-20",
            "cnpj": "123456",
            "cnpj_root": "123456",
            "retail_store_tags": [{"name": "tag2"}, {"name": "tag1"}],
            "retail_store_phones": [
                {"value": "56666133854", "phone_type": 2},
                {"value": "55561199854", "phone_type": 1},
            ],
            "retail_store_address": [
                {
                    "address_type": "MAIN",
                    "city": "SÃO PAULO",
                    "state_or_province": "SP",
                    "street_with_house_number_or_name": "Rua com o número",
                    "neighborhood": "Vila Indiana",
                    "country": "Brasil",
                    "postal_code": "12344567",
                    "mesoregion": "Meso Region",
                    "microregion": "Micro Region",
                    "city_council_code": "1234",
                }
            ],
            "retail_store_dealer": [
                {
                    "dealer_email": [{"email": "email 2"}, {"email": "email 1"}],
                    "dealer_phones": [
                        {"value": "56666933854", "phone_type": 2},
                        {"value": "55566999854", "phone_type": 1},
                    ],
                }
            ],
            "industry_id": "83c81318-bd76-435f-b4b0-1c8dd1e79849",
        }

        store = RetailStore(
            id="74633baa-3063-4537-9eca-71a7af212d6f",
            social_name="Nome social",
            erp_code="123",
            business_region="test de regiao",
            registered_at_partner="2019-02-20",
            cnpj="123456",
            cnpj_root="123456",
            industry_id="83c81318-bd76-435f-b4b0-1c8dd1e79849",
            retail_store_dealer=[
                RetailStoreDealer(
                    retail_store_dealer_emails=[
                        RetailStoreDealerEmail(email="email 2"),
                        RetailStoreDealerEmail(email="email 1"),
                    ],
                    retail_store_dealer_phones=[
                        RetailStoreDealerPhone(value="56666933854", phone_type=2),
                        RetailStoreDealerPhone(value="55566999854", phone_type=1),
                    ],
                )
            ],
            retail_store_tags=[RetailStoreTag(name="tag2"), RetailStoreTag(name="tag1")],
            retail_store_phones=[
                RetailStorePhone(value="56666133854", phone_type=2),
                RetailStorePhone(value="55561199854", phone_type=1),
            ],
            retail_store_address=[
                RetailStoreAddress(
                    address_type="MAIN",
                    city="SÃO PAULO",
                    state_or_province="SP",
                    street_with_house_number_or_name="Rua com o número",
                    neighborhood="Vila Indiana",
                    country="Brasil",
                    postal_code="12344567",
                    mesoregion="Meso Region",
                    microregion="Micro Region",
                    city_council_code="1234",
                )
            ],
        )

        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.put(f"{HOST}retailstore/74633baa-3063-4537-9eca-71a7af212d6f/", json={})

            model = RetailStore()
            model.objects.update(store)

            self.assertEqual(m.request_history[1].method, "PUT")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_retail_store_body)

    def test_create_retail_store(self):
        expected_retail_store_body = {
            "social_name": "Nome social",
            "erp_code": "123",
            "business_region": "test de regiao",
            "registered_at_partner": "2019-02-20",
            "cnpj": "123456",
            "cnpj_root": "123456",
            "direct": True,
            "retail_store_tags": [{"name": "tag2"}, {"name": "tag1"}],
            "retail_store_phones": [
                {"value": "56666133854", "phone_type": 2},
                {"value": "55561199854", "phone_type": 1},
            ],
            "retail_store_address": [
                {
                    "address_type": "MAIN",
                    "city": "SÃO PAULO",
                    "state_or_province": "SP",
                    "street_with_house_number_or_name": "Rua com o número",
                    "neighborhood": "Vila Indiana",
                    "country": "Brasil",
                    "postal_code": "12344567",
                    "mesoregion": "Meso Region",
                    "microregion": "Micro Region",
                    "city_council_code": "1234",
                }
            ],
            "retail_store_dealer": [
                {
                    "dealer_email": [{"email": "email 2"}, {"email": "email 1"}],
                    "dealer_phones": [
                        {"value": "56666933854", "phone_type": 2},
                        {"value": "55566999854", "phone_type": 1},
                    ],
                }
            ],
            "industry_id": "83c81318-bd76-435f-b4b0-1c8dd1e79849",
        }

        with requests_mock.Mocker() as m:

            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.post(f"{HOST}retailstore/", status_code=201, json={"id": "uuid-post"})

            model = RetailStore()

            model.objects.create(
                social_name="Nome social",
                erp_code="123",
                business_region="test de regiao",
                registered_at_partner="2019-02-20",
                cnpj="123456",
                cnpj_root="123456",
                industry_id="83c81318-bd76-435f-b4b0-1c8dd1e79849",
                direct=True,
                retail_store_dealer=[
                    RetailStoreDealer(
                        retail_store_dealer_emails=[
                            RetailStoreDealerEmail(email="email 2"),
                            RetailStoreDealerEmail(email="email 1"),
                        ],
                        retail_store_dealer_phones=[
                            RetailStoreDealerPhone(value="56666933854", phone_type=2),
                            RetailStoreDealerPhone(value="55566999854", phone_type=1),
                        ],
                    )
                ],
                retail_store_tags=[RetailStoreTag(name="tag2"), RetailStoreTag(name="tag1")],
                retail_store_phones=[
                    RetailStorePhone(value="56666133854", phone_type=2),
                    RetailStorePhone(value="55561199854", phone_type=1),
                ],
                retail_store_address=[
                    RetailStoreAddress(
                        address_type="MAIN",
                        city="SÃO PAULO",
                        state_or_province="SP",
                        street_with_house_number_or_name="Rua com o número",
                        neighborhood="Vila Indiana",
                        country="Brasil",
                        postal_code="12344567",
                        mesoregion="Meso Region",
                        microregion="Micro Region",
                        city_council_code="1234",
                    )
                ],
            )

            self.assertTrue(m.called)
            self.assertEqual(m.call_count, 2)

            self.assertEqual(m.request_history[1].method, "POST")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_retail_store_body)

    def test_delete_retail_store(self):
        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = RetailStore()

            with self.assertRaises(NotImplementedError):
                model.objects.delete()
