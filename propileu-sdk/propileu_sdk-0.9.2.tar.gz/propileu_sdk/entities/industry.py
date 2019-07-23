from __future__ import annotations

from typing import List
from typing import Optional

from propileu_sdk.entities.base_manager import BaseManager


class Industry:
    ENDPOINT = "industry"

    def __init__(self, id: str = None, name: str = None, request_id: str = None):
        self.id = id
        self.name = name
        self.objects = Industry.Manager(request_id=request_id)

    class Manager(BaseManager):
        def create(self, name: str) -> dict:
            base_dict = {"name": name}

            return self.execute_post(f"{Industry.ENDPOINT}/", base_dict)

        def get(self, id: str) -> Optional[Industry]:
            base_dict = self.execute_get(f"{Industry.ENDPOINT}/{id}/")

            if base_dict:
                return Industry(**base_dict)

            return None

        def filter(self, name: str = None) -> List[Industry]:
            params = {"name": name}
            base_list = self.execute_get(f"{Industry.ENDPOINT}/", params)
            base_list = base_list["results"]
            return [Industry(**base_dict) for base_dict in base_list]

        def update(self, industry: Industry) -> dict:
            base_dict = {"id": industry.id, "name": industry.name}

            return self.execute_put(f"{Industry.ENDPOINT}/{industry.id}/", base_dict)

        def delete(self) -> None:
            raise NotImplementedError
