from __future__ import annotations

from typing import List
from typing import Optional

from propileu_sdk.entities.base_manager import BaseManager


class Product:
    ENDPOINT = "product"

    def __init__(
        self,
        id: str = None,
        sku: str = None,
        family_id: str = None,
        conversion_factor: str = None,
        request_id: str = None,
        description: str = None,
        industry_id: str = None,
        direct: bool = False,
    ):
        self.id = id
        self.sku = sku
        self.family_id = family_id
        self.conversion_factor = conversion_factor
        self.description = description
        self.industry_id = industry_id
        self.direct = direct
        self.objects = Product.Manager(request_id=request_id)

    class Manager(BaseManager):
        def create(
            self,
            sku: str,
            family_id: str,
            conversion_factor: str,
            description: str,
            industry_id: str,
            direct: bool = False,
        ) -> dict:
            base_dict = {
                "sku": sku,
                "family_id": family_id,
                "conversion_factor": conversion_factor,
                "description": description,
                "industry_id": industry_id,
                "direct": direct,
            }
            return self.execute_post(f"{Product.ENDPOINT}/", base_dict)

        def get(self, id: str) -> Optional[Product]:
            base_dict = self.execute_get(f"{Product.ENDPOINT}/{id}/")

            if base_dict:
                return Product(**base_dict)

            return None

        def filter(self, sku: str = None, family_id: str = None, industry_id: str = None) -> List[Product]:
            params = {"sku": sku, "family_id": family_id, "industry_id": industry_id}
            base_list = self.execute_get(f"{Product.ENDPOINT}/", params)

            base_list = base_list["results"]
            return [Product(**base_dict) for base_dict in base_list]

        def update(self, product: Product) -> dict:
            base_dict = {
                "id": product.id,
                "sku": product.sku,
                "family_id": product.family_id,
                "conversion_factor": product.conversion_factor,
                "description": product.description,
                "industry_id": product.industry_id,
                "direct": product.direct,
            }

            return self.execute_put(f"{Product.ENDPOINT}/{product.id}/", base_dict)

        def delete(self) -> None:
            raise NotImplementedError


class ProductFamily:
    ENDPOINT = "productfamily"

    def __init__(
        self,
        id: str = None,
        name: str = None,
        conversion_factor: str = None,
        industry_id: str = None,
        request_id: str = None,
    ):
        self.id = id
        self.name = name
        self.industry_id = industry_id
        self.conversion_factor = conversion_factor
        self.objects = ProductFamily.Manager(request_id=request_id)

    class Manager(BaseManager):
        def create(self, name: str, industry_id: str, conversion_factor: str) -> None:
            base_dict = {"name": name, "industry_id": industry_id, "conversion_factor": conversion_factor}

            return self.execute_post(f"{ProductFamily.ENDPOINT}/", base_dict)

        def get(self, id: str) -> Optional[ProductFamily]:
            base_dict = self.execute_get(f"{ProductFamily.ENDPOINT}/{id}/")

            if base_dict:
                return ProductFamily(**base_dict)

            return None

        def filter(
            self, name: str = None, industry_id: str = None, conversion_factor: str = None
        ) -> List[ProductFamily]:
            params = {"name": name, "industry_id": industry_id, "conversion_factor": conversion_factor}
            base_list = self.execute_get(f"{ProductFamily.ENDPOINT}/", params)

            base_list = base_list["results"]
            return [ProductFamily(**base_dict) for base_dict in base_list]

        def update(self, product_family: ProductFamily) -> None:
            base_dict = {
                "id": product_family.id,
                "name": product_family.name,
                "industry_id": product_family.industry_id,
                "conversion_factor": product_family.conversion_factor,
            }

            return self.execute_put(f"{ProductFamily.ENDPOINT}/{product_family.id}/", base_dict)

        def delete(self) -> None:
            raise NotImplementedError
