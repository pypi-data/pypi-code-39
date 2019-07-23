from __future__ import annotations

from typing import List
from typing import Optional

from propileu_sdk.entities.base_manager import BaseManager


class Office:
    ENDPOINT = "office"

    def __init__(
        self,
        id: str = None,
        name: str = None,
        erp_code: str = None,
        industry_id: str = None,
        request_id: str = None,
        direct: bool = False,
    ):
        self.id = id
        self.name = name
        self.erp_code = erp_code
        self.industry_id = industry_id
        self.objects = Office.Manager(request_id=request_id)
        self.direct = direct

    class Manager(BaseManager):
        def create(self, name: str, erp_code: str, industry_id, direct: bool = False) -> dict:
            base_dict = {"name": name, "erp_code": erp_code, "industry_id": industry_id, "direct": direct}

            return self.execute_post(f"{Office.ENDPOINT}/", base_dict)

        def get(self, id: str) -> Optional[Office]:
            base_dict = self.execute_get(f"{Office.ENDPOINT}/{id}/")

            if base_dict:
                return Office(**base_dict)

            return None

        def filter(self, name: str = None, erp_code: str = None, industry_id: str = None) -> List[Office]:
            params = {"name": name, "erp_code": erp_code, "industry_id": industry_id}
            base_list = self.execute_get(f"{Office.ENDPOINT}/", params)

            base_list = base_list["results"]
            return [Office(**base_dict) for base_dict in base_list]

        def update(self, office: Office) -> dict:
            base_dict = {
                "id": office.id,
                "name": office.name,
                "erp_code": office.erp_code,
                "industry_id": office.industry_id,
                "direct": office.direct,
            }

            return self.execute_put(f"{Office.ENDPOINT}/{office.id}/", base_dict)

        def delete(self) -> None:
            raise NotImplementedError
