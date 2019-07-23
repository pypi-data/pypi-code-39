from __future__ import annotations

from typing import List
from typing import Optional

from propileu_sdk.entities.base_manager import BaseManager


class EmployeeRetailStore:
    ENDPOINT = "retailstoreemployee"

    def __init__(
        self,
        id: str = None,
        industry_id: str = None,
        customer_id: str = None,
        employee_id: str = None,
        sales_office_id: str = None,
        coordinator_id: str = None,
        region_id: str = None,
        request_id: str = None,
        direct: bool = True,
    ):
        self.id = id
        self.industry_id = industry_id
        self.customer_id = customer_id
        self.employee_id = employee_id
        self.sales_office_id = sales_office_id
        self.coordinator_id = coordinator_id
        self.region_id = region_id
        self.objects = EmployeeRetailStore.Manager(request_id=request_id)
        self.direct = direct

    class Manager(BaseManager):
        def create(
            self,
            industry_id: str = None,
            customer_id: str = None,
            employee_id: str = None,
            sales_office_id: str = None,
            coordinator_id: str = None,
            region_id: str = None,
            direct: bool = True,
        ) -> dict:
            base_dict = {
                "industry_id": industry_id,
                "customer_id": customer_id,
                "employee_id": employee_id,
                "sales_office_id": sales_office_id,
                "coordinator_id": coordinator_id,
                "region_id": region_id,
                "direct": direct,
            }
            return self.execute_post(f"{EmployeeRetailStore.ENDPOINT}/", base_dict)

        def get(self, id: str) -> Optional[EmployeeRetailStore]:
            base_dict = self.execute_get(f"{EmployeeRetailStore.ENDPOINT}/{id}/")

            if base_dict:
                return EmployeeRetailStore(**base_dict)

            return None

        def filter(
            self,
            industry_id: str = None,
            customer_id: str = None,
            employee_id: str = None,
            sales_office_id: str = None,
            coordinator_id: str = None,
            region_id: str = None,
        ) -> List[EmployeeRetailStore]:
            params = {
                "industry_id": industry_id,
                "customer_id": customer_id,
                "employee_id": employee_id,
                "sales_office_id": sales_office_id,
                "coordinator_id": coordinator_id,
                "region_id": region_id,
            }
            base_list = self.execute_get(f"{EmployeeRetailStore.ENDPOINT}/", params)
            return [EmployeeRetailStore(**base_dict) for base_dict in base_list["results"]]

        def update(self, employee_retail_store: EmployeeRetailStore) -> dict:
            base_dict = {
                "id": employee_retail_store.id,
                "industry_id": employee_retail_store.industry_id,
                "customer_id": employee_retail_store.customer_id,
                "employee_id": employee_retail_store.employee_id,
                "sales_office_id": employee_retail_store.sales_office_id,
                "coordinator_id": employee_retail_store.coordinator_id,
                "region_id": employee_retail_store.region_id,
                "direct": employee_retail_store.direct,
            }
            return self.execute_put(f"{EmployeeRetailStore.ENDPOINT}/{employee_retail_store.id}/", base_dict)

        def delete(self, id: str) -> None:
            raise NotImplementedError
