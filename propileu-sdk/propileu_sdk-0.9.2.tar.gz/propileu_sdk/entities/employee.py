from __future__ import annotations

from typing import List
from typing import Optional

from propileu_sdk.entities.base_manager import BaseManager


class EmployeePhone(dict):
    def __init__(self, phone_type: int = None, value: str = None):
        dict.__init__(self, id=id, phone_type=phone_type, value=value)
        self.phone_type = phone_type
        self.value = value


class EmployeeDocument(dict):
    def __init__(self, document_type: int = None, value: str = None):
        dict.__init__(self, id=id, document_type=document_type, value=value)
        self.document_type = document_type
        self.value = value


class EmployeeEmail(dict):
    def __init__(self, email: str = None):
        dict.__init__(self, id=id, email=email)
        self.email = email


class Employee:
    ENDPOINT = "employee"

    def __init__(
        self,
        id: str = None,
        erp_code: str = None,
        name: str = None,
        industry_id: str = None,
        request_id: str = None,
        emails: List[EmployeeEmail] = [],
        phones: List[EmployeePhone] = [],
        documents: List[EmployeeDocument] = [],
        employee_code: str = None,
        direct: bool = False,
    ):
        self.id = id
        self.erp_code = erp_code
        self.name = name
        self.industry_id = industry_id
        self.objects = Employee.Manager(request_id=request_id)
        self.emails = emails
        self.phones = phones
        self.documents = documents
        self.direct = direct

    class Manager(BaseManager):
        def create(
            self,
            erp_code: str = None,
            name: str = None,
            industry_id: str = None,
            emails: List[EmployeeEmail] = [],
            phones: List[EmployeePhone] = [],
            documents: List[EmployeeDocument] = [],
            direct: bool = False,
        ) -> dict:
            base_dict = {
                "industry_id": industry_id,
                "name": name,
                "documents": [{"value": d["value"], "document_type": d["document_type"]} for d in documents],
                "emails": [{"email": e["email"]} for e in emails],
                "phones": [{"value": p["value"], "phone_type": p["phone_type"]} for p in phones],
                "erp_code": erp_code,
                "direct": direct,
            }

            return self.execute_post(f"{Employee.ENDPOINT}/", base_dict)

        def get(self, id: str) -> Optional[Employee]:
            base_dict = self.execute_get(f"{Employee.ENDPOINT}/{id}/")

            if base_dict:
                emails = []
                phones = []
                documents = []
                for email in base_dict["emails"]:
                    emails.append(EmployeeEmail(email=email["email"]))
                for phone in base_dict["phones"]:
                    phones.append(EmployeePhone(value=phone["value"], phone_type=phone["phone_type"]))
                for document in base_dict["documents"]:
                    documents.append(EmployeeDocument(value=document["value"], document_type=document["document_type"]))

                base_dict.pop("emails")
                base_dict.pop("phones")
                base_dict.pop("documents")
                return Employee(**base_dict, phones=phones, emails=emails, documents=documents)

            return None

        def filter(
            self, name: str = None, documents__value: str = None, industry_id: str = None, erp_code: str = None
        ) -> List[Employee]:
            params = {
                "name": name,
                "documents__value": documents__value,
                "industry_id": industry_id,
                "erp_code": erp_code,
            }
            base_list = self.execute_get(f"{Employee.ENDPOINT}/", params)
            base_list = base_list["results"]

            employees = []
            for employee in base_list:
                emails = []
                phones = []
                documents = []
                for email in employee["emails"]:
                    emails.append(EmployeeEmail(email=email["email"]))
                for phone in employee["phones"]:
                    phones.append(EmployeePhone(value=phone["value"], phone_type=phone["phone_type"]))
                for document in employee["documents"]:
                    documents.append(EmployeeDocument(value=document["value"], document_type=document["document_type"]))

                employee.pop("emails")
                employee.pop("phones")
                employee.pop("documents")
                employees.append(Employee(**employee, phones=phones, emails=emails, documents=documents))

            return employees

        def update(self, employee: Employee) -> dict:
            base_dict = {
                "id": employee.id,
                "industry_id": employee.industry_id,
                "name": employee.name,
                "documents": [{"value": d["value"], "document_type": d["document_type"]} for d in employee.documents],
                "emails": [{"email": e["email"]} for e in employee.emails],
                "phones": [{"value": p["value"], "phone_type": p["phone_type"]} for p in employee.phones],
                "erp_code": employee.erp_code,
                "direct": employee.direct,
            }

            return self.execute_put(f"{Employee.ENDPOINT}/{employee.id}/", base_dict)

        def delete(self) -> None:
            raise NotImplementedError
