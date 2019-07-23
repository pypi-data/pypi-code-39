import json
from unittest import TestCase

import requests_mock

from propileu_sdk.config import HOST
from propileu_sdk.config import HOST_AUTH
from propileu_sdk.entities.base_manager import _authentication_logic
from propileu_sdk.sdk import Employee
from propileu_sdk.sdk import EmployeeDocument
from propileu_sdk.sdk import EmployeeEmail
from propileu_sdk.sdk import EmployeePhone


class EmployeeTest(TestCase):
    def setUp(self) -> None:
        _authentication_logic.token = None

    def test_get_a_employee(self):
        billing_mock = {
            "id": "d4484dc0-3df1-42fa-bd0a-13e5512b9992",
            "industry_id": "6aeb0323-3932-412c-bd45-ad8e159754f7",
            "name": "Ricardo",
            "documents": [{"value": "19265899447", "document_type": 1}],
            "emails": [{"email": "email@email.com"}],
            "phones": [{"value": "11995568874", "phone_type": 1}],
            "erp_code": "123",
            "direct": True,
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}employee/d4484dc0-3df1-42fa-bd0a-13e5512b9992/", json=billing_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Employee()
            model_result = model.objects.get("d4484dc0-3df1-42fa-bd0a-13e5512b9992")

            self.assertEqual(model_result.id, "d4484dc0-3df1-42fa-bd0a-13e5512b9992")
            self.assertEqual(model_result.erp_code, "123")
            self.assertEqual(model_result.name, "Ricardo")
            self.assertEqual(model_result.industry_id, "6aeb0323-3932-412c-bd45-ad8e159754f7")
            self.assertTrue(model_result.direct)
            self.assertIsInstance(model_result.emails[0], EmployeeEmail)
            self.assertIsInstance(model_result.phones[0], EmployeePhone)
            self.assertIsInstance(model_result.documents[0], EmployeeDocument)

            self.assertEqual(model_result.emails[0].email, "email@email.com")
            self.assertEqual(model_result.phones[0].phone_type, 1)
            self.assertEqual(model_result.phones[0].value, "11995568874")
            self.assertEqual(model_result.documents[0].document_type, 1)
            self.assertEqual(model_result.documents[0].value, "19265899447")

            self.assertEqual(len(model_result.emails), 1)
            self.assertEqual(len(model_result.phones), 1)
            self.assertEqual(len(model_result.documents), 1)

    def test_get_not_found_employee(self):
        with requests_mock.Mocker() as m:
            m.get(f"{HOST}employee/4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3/", status_code=404)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            model = Employee()
            model_rslt = model.objects.get("4b9af65f-c923-4fc7-aa06-85c2c9ea8bd3")

            self.assertIsNone(model_rslt)

    def test_filter_employee(self):
        json_mock = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "97415eba-7350-4fbf-abb7-934424ddcdb1",
                    "industry_id": "11de2031-cffb-42d2-ae9a-377cb7b36429",
                    "name": "Will",
                    "documents": [],
                    "emails": [],
                    "phones": [],
                    "erp_code": "",
                    "direct": True,
                },
                {
                    "id": "d4484dc0-3df1-42fa-bd0a-13e5512b9992",
                    "industry_id": "6aeb0323-3932-412c-bd45-ad8e159754f7",
                    "name": "Ricardo",
                    "documents": [{"value": "19265899447", "document_type": 1}],
                    "emails": [{"email": "email@email.com"}],
                    "phones": [{"value": "11995568874", "phone_type": 1}],
                    "erp_code": "",
                },
            ],
        }

        with requests_mock.Mocker() as m:
            m.get(f"{HOST}employee/?name=Will", json=json_mock)
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Employee()
            model_result = model.objects.filter(name="Will")

            self.assertEqual(model_result[0].name, "Will")
            self.assertEqual(model_result[0].id, "97415eba-7350-4fbf-abb7-934424ddcdb1")
            self.assertEqual(model_result[0].industry_id, "11de2031-cffb-42d2-ae9a-377cb7b36429")
            self.assertTrue(model_result[0].direct)
            self.assertEqual(len(model_result[0].emails), 0)
            self.assertEqual(len(model_result[0].documents), 0)
            self.assertEqual(len(model_result[0].phones), 0)

            self.assertEqual(model_result[1].name, "Ricardo")
            self.assertEqual(model_result[1].id, "d4484dc0-3df1-42fa-bd0a-13e5512b9992")
            self.assertEqual(model_result[1].industry_id, "6aeb0323-3932-412c-bd45-ad8e159754f7")
            self.assertEqual(len(model_result[1].emails), 1)
            self.assertEqual(len(model_result[1].documents), 1)
            self.assertEqual(len(model_result[1].phones), 1)

            self.assertEqual(model_result[1].emails[0].email, "email@email.com")
            self.assertEqual(model_result[1].documents[0].value, "19265899447")
            self.assertEqual(model_result[1].phones[0].value, "11995568874")
            self.assertEqual(model_result[1].documents[0].document_type, 1)
            self.assertEqual(model_result[1].phones[0].phone_type, 1)

            self.assertEqual(len(model_result), 2)

    def test_update_employee(self):
        expected_employee_body = {
            "id": "d4484dc0-3df1-42fa-bd0a-13e5512b9992",
            "industry_id": "6aeb0323-3932-412c-bd45-ad8e159754f7",
            "name": "Ricardo",
            "documents": [{"value": "19265899447", "document_type": 1}],
            "emails": [{"email": "email@email.com"}],
            "phones": [{"value": "11995568874", "phone_type": 1}],
            "erp_code": "123",
            "direct": True,
        }

        employee = Employee(
            id="d4484dc0-3df1-42fa-bd0a-13e5512b9992",
            industry_id="6aeb0323-3932-412c-bd45-ad8e159754f7",
            name="Ricardo",
            direct=True,
            documents=[],
            emails=[],
            phones=[],
            erp_code="123",
        )

        employee.emails = [EmployeeEmail(email="email@email.com")]
        employee.phones = [EmployeePhone(value="11995568874", phone_type=1)]
        employee.documents = [EmployeeDocument(value="19265899447", document_type=1)]

        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.put(f"{HOST}employee/d4484dc0-3df1-42fa-bd0a-13e5512b9992/", json={"id": "uuid-put"})

            model = Employee()
            model.objects.update(employee=employee)

            self.assertEqual(m.request_history[1].method, "PUT")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_employee_body)

    def test_create_employee(self):
        expected_employee_body = {
            "industry_id": "6aeb0323-3932-412c-bd45-ad8e159754f7",
            "name": "Ricardo",
            "documents": [{"value": "19265899447", "document_type": 1}],
            "emails": [{"email": "email@email.com"}],
            "phones": [{"value": "11995568874", "phone_type": 1}],
            "erp_code": "123",
            "direct": True,
        }

        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})
            m.post(f"{HOST}employee/", status_code=201, json={"id": "uuid-post"})

            model = Employee()

            model.objects.create(
                industry_id="6aeb0323-3932-412c-bd45-ad8e159754f7",
                name="Ricardo",
                documents=[EmployeeDocument(value="19265899447", document_type=1)],
                emails=[EmployeeEmail(email="email@email.com")],
                phones=[EmployeePhone(value="11995568874", phone_type=1)],
                erp_code="123",
                direct=True,
            )

            self.assertTrue(m.called)
            self.assertEqual(m.call_count, 2)

            self.assertEqual(m.request_history[1].method, "POST")
            self.assertDictEqual(json.loads(m.request_history[1].body), expected_employee_body)

    def test_delete_employee(self):
        with requests_mock.Mocker() as m:
            m.post(f"{HOST_AUTH}", json={"token": "token123"})

            model = Employee()

            with self.assertRaises(NotImplementedError):
                model.objects.delete()
