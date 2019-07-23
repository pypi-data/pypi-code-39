from __future__ import annotations

from typing import List
from typing import Optional

from propileu_sdk.entities.base_manager import BaseManager


class Regions:
    ENDPOINT = "regions"

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
        self.industry_id = industry_id
        self.erp_code = erp_code
        self.objects = Regions.Manager(request_id=request_id)
        self.direct = direct

    class Manager(BaseManager):
        def create(self, name: str, industry_id: str, erp_code: str, direct: bool = False) -> dict:
            base_dict = {"name": name, "industry_id": industry_id, "erp_code": erp_code, "direct": direct}
            return self.execute_post(f"{Regions.ENDPOINT}/", base_dict)

        def get(self, id: str) -> Optional[Regions]:
            base_dict = self.execute_get(f"{Regions.ENDPOINT}/{id}/")
            if base_dict:
                return Regions(**base_dict)
            return None

        def filter(self, name: str = None, industry_id: str = None, erp_code: str = None) -> List[Regions]:
            params = {"name": name, "industry_id": industry_id, "erp_code": erp_code}
            base_list = self.execute_get(f"{Regions.ENDPOINT}/", params)

            base_list = base_list["results"]
            return [Regions(**base_dict) for base_dict in base_list]

        def update(self, regions: Regions) -> dict:
            base_dict = {
                "id": regions.id,
                "name": regions.name,
                "industry_id": regions.industry_id,
                "erp_code": regions.erp_code,
                "direct": regions.direct,
            }

            return self.execute_put(f"{Regions.ENDPOINT}/{regions.id}/", base_dict)

        def delete(self) -> None:
            raise NotImplementedError
