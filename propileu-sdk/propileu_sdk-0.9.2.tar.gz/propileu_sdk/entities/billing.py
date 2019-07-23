from __future__ import annotations

import logging
from typing import List
from typing import Optional

from propileu_sdk.entities.base_manager import BaseManager


class BillingItens:
    def __init__(
        self,
        id: str = None,
        value: str = None,
        units: str = None,
        mass: str = None,
        bulk_type: str = None,
        product_id: str = None,
        sku: str = None,
    ):
        self.id = id
        self.value = value
        self.units = units
        self.mass = mass
        self.bulk_type = bulk_type
        self.product_id = product_id
        self.sku = sku


class Billing:
    ENDPOINT = "billing"

    def __init__(
        self,
        id: str = None,
        erp_code: str = None,
        billing_date: str = None,
        industry_id: str = None,
        value: float = None,
        store_issuer_id: str = None,
        store_receiver_id: str = None,
        request_id: str = None,
        billing_item: List[BillingItens] = None,
        billing_type: str = None,
        employee_code: str = None,
        direct: bool = False,
    ):
        self.id = id
        self.billing_date = billing_date
        self.store_issuer_id = store_issuer_id
        self.store_receiver_id = store_receiver_id
        self.industry_id = industry_id
        self.erp_code = erp_code
        self.value = value
        self.billing_item = billing_item
        self.billing_type = billing_type
        self.employee_code = employee_code
        self.objects = Billing.Manager(request_id=request_id)
        self.direct = direct

    class Manager(BaseManager):
        def create(
            self,
            erp_code: str = None,
            billing_date: str = None,
            industry_id: str = None,
            value: float = None,
            store_issuer_id: str = None,
            store_receiver_id: str = None,
            billing_type: str = None,
            billing_item: List[BillingItens] = [],
            employee_code: str = None,
            direct: bool = False,
        ) -> dict:

            base_dict = {
                "erp_code": erp_code,
                "industry_id": industry_id,
                "billing_date": billing_date,
                "value": value,
                "store_issuer_id": store_issuer_id,
                "store_receiver_id": store_receiver_id,
                "billing_type": billing_type,
                "employee_code": employee_code,
                "billing_item": [],
                "direct": direct,
            }
            for item in billing_item:
                base_dict["billing_item"].append(
                    {
                        "value": item.value,
                        "units": item.units,
                        "mass": item.mass,
                        "bulk_type": item.bulk_type,
                        "product_id": item.product_id,
                        "sku": item.sku,
                    }
                )

            logging.debug(base_dict)
            return self.execute_post(f"{Billing.ENDPOINT}/", base_dict)

        def get(self, id: str) -> Optional[Billing]:
            base_dict = self.execute_get(f"{Billing.ENDPOINT}/{id}/")

            if base_dict:
                itens = []
                for item in base_dict["billing_item"]:
                    itens.append(BillingItens(**item))
                base_dict.pop("billing_item")
                billing = Billing(**base_dict, billing_item=itens)
                return billing

            return None

        def filter(
            self,
            erp_code: str = None,
            billing_date: str = None,
            industry_id: str = None,
            value: str = None,
            store_issuer_id: str = None,
            store_receiver_id: str = None,
            billing_type: str = None,
            units_item: str = None,
            sku_item: str = None,
        ) -> List[Billing]:
            params = {
                "erp_code": erp_code,
                "billing_date": billing_date,
                "industry_id": industry_id,
                "value": value,
                "store_issuer_id": store_issuer_id,
                "store_receiver_id": store_receiver_id,
                "billing_type": billing_type,
                "units_item": units_item,
                "sku_item": sku_item,
            }
            base_list = self.execute_get(f"{Billing.ENDPOINT}/", params)
            base_list = base_list["results"]

            billing_list = []
            for billing in base_list:
                itens = []
                for item in billing["billing_item"]:
                    item.pop("id")
                    itens.append(BillingItens(**item))
                billing.pop("billing_item")
                billing_list.append(Billing(**billing, billing_item=itens))

            return billing_list

        def update(self, billing: Billing) -> dict:
            base_dict = {
                "id": billing.id,
                "billing_date": billing.billing_date,
                "industry_id": billing.industry_id,
                "value": billing.value,
                "store_issuer_id": billing.store_issuer_id,
                "store_receiver_id": billing.store_receiver_id,
                "erp_code": billing.erp_code,
                "billing_item": [],
                "billing_type": billing.billing_type,
                "employee_code": billing.employee_code,
                "direct": True,
            }

            for item in billing.billing_item:
                base_dict["billing_item"].append(
                    {
                        "id": item.id,
                        "value": item.value,
                        "units": item.units,
                        "mass": item.mass,
                        "bulk_type": item.bulk_type,
                        "product_id": item.product_id,
                        "sku": item.sku,
                    }
                )

            return self.execute_put(f"{Billing.ENDPOINT}/{billing.id}/", base_dict)

        def delete(self) -> None:
            raise NotImplementedError()
