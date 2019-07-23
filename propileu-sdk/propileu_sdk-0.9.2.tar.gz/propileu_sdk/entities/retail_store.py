from __future__ import annotations

from typing import List
from typing import Optional
from typing import Union

from propileu_sdk.entities.base_manager import BaseManager


class RetailStoreAddress(dict):
    def __init__(
        self,
        address_type: Union[str, int] = None,
        city: str = None,
        state_or_province: str = None,
        street_with_house_number_or_name: str = None,
        neighborhood: str = None,
        country: str = None,
        postal_code: str = None,
        mesoregion: str = None,
        microregion: str = None,
        city_council_code: str = None,
    ):
        dict.__init__(
            self,
            address_type=address_type,
            city=city,
            state_or_province=state_or_province,
            street_with_house_number_or_name=street_with_house_number_or_name,
            neighborhood=neighborhood,
            country=country,
            postal_code=postal_code,
            mesoregion=mesoregion,
            microregion=microregion,
            city_council_code=city_council_code,
        )
        self.address_type = address_type
        self.city = city
        self.state_or_province = state_or_province
        self.street_with_house_number_or_name = street_with_house_number_or_name
        self.neighborhood = neighborhood
        self.country = country
        self.postal_code = postal_code
        self.mesoregion = mesoregion
        self.microregion = microregion
        self.city_council_code = city_council_code


class RetailStorePhone(dict):
    def __init__(self, phone_type: int = None, value: str = None):
        dict.__init__(self, phone_type=phone_type, value=value)
        self.phone_type = phone_type
        self.value = value


class RetailStoreTag(dict):
    def __init__(self, id: str = None, name: str = None):
        dict.__init__(self, id=id, name=name)
        self.name = name


class RetailStoreDealerEmail(dict):
    def __init__(self, email: str = None):
        dict.__init__(self, email=email)
        self.email = email


class RetailStoreDealerPhone(dict):
    def __init__(self, phone_type: int = None, value: str = None):
        dict.__init__(self, phone_type=phone_type, value=value)
        self.phone_type = phone_type
        self.value = value


class RetailStoreDealer(dict):
    def __init__(
        self,
        retail_store_dealer_emails: List[RetailStoreDealerEmail] = None,
        retail_store_dealer_phones: List[RetailStoreDealerPhone] = None,
    ):
        dict.__init__(
            self,
            retail_store_dealer_emails=retail_store_dealer_emails,
            retail_store_dealer_phones=retail_store_dealer_phones,
        )
        self.retail_store_dealer_emails = retail_store_dealer_emails
        self.retail_store_dealer_phones = retail_store_dealer_phones


class RetailStore:
    ENDPOINT = "retailstore"

    def __init__(
        self,
        id: str = None,
        retail_store_dealer: List[RetailStoreDealer] = [],
        retail_store_tags: List[RetailStoreTag] = [],
        retail_store_phones: List[RetailStorePhone] = [],
        retail_store_address: List[RetailStoreAddress] = [],
        social_name: str = None,
        erp_code: str = None,
        business_region: str = None,
        registered_at_partner: str = None,
        cnpj: str = None,
        cnpj_root: str = None,
        industry_id: str = None,
        request_id: str = None,
        direct: bool = False,
    ):
        self.id = id
        self.social_name = social_name
        self.erp_code = erp_code
        self.business_region = business_region
        self.registered_at_partner = registered_at_partner
        self.cnpj = cnpj
        self.cnpj_root = cnpj_root
        self.industry_id = industry_id
        self.retail_store_dealer = retail_store_dealer
        self.retail_store_tags = retail_store_tags
        self.retail_store_phones = retail_store_phones
        self.retail_store_address = retail_store_address
        self.direct = direct

        self.objects = RetailStore.Manager(request_id=request_id)

    class Manager(BaseManager):
        def create(
            self,
            social_name: str,
            erp_code: str,
            business_region: str,
            registered_at_partner: str,
            cnpj: str,
            cnpj_root: str,
            industry_id: str,
            retail_store_tags: List[RetailStoreTag],
            retail_store_dealer: List[RetailStoreDealer],
            retail_store_phones: List[RetailStorePhone],
            retail_store_address: List[RetailStoreAddress],
            direct: bool,
        ) -> dict:

            base_dict = {
                "social_name": social_name,
                "erp_code": erp_code,
                "business_region": business_region,
                "registered_at_partner": registered_at_partner,
                "cnpj": cnpj,
                "cnpj_root": cnpj_root,
                "industry_id": industry_id,
                "direct": direct,
                "retail_store_tags": [{"name": t.name} for t in retail_store_tags],
                "retail_store_dealer": [],
                "retail_store_phones": [
                    {"value": p["value"], "phone_type": p["phone_type"]} for p in retail_store_phones
                ],
                "retail_store_address": [
                    {
                        "address_type": a["address_type"],
                        "city": a["city"],
                        "state_or_province": a["state_or_province"],
                        "street_with_house_number_or_name": a["street_with_house_number_or_name"],
                        "neighborhood": a["neighborhood"],
                        "country": a["country"],
                        "postal_code": a["postal_code"],
                        "mesoregion": a["mesoregion"],
                        "microregion": a["microregion"],
                        "city_council_code": a["city_council_code"],
                    }
                    for a in retail_store_address
                ],
            }

            for d in retail_store_dealer:
                dealer_dict = {"dealer_email": [], "dealer_phones": []}
                for email in d["retail_store_dealer_emails"]:
                    dealer_dict["dealer_email"].append({"email": email.email})

                for phone in d["retail_store_dealer_phones"]:
                    dealer_dict["dealer_phones"].append({"value": phone["value"], "phone_type": phone["phone_type"]})

                base_dict["retail_store_dealer"].append(dealer_dict)

            return self.execute_post(f"{RetailStore.ENDPOINT}/", base_dict)

        def get(self, id: str) -> Optional[RetailStore]:
            base_dict = self.execute_get(f"{RetailStore.ENDPOINT}/{id}/")

            if base_dict:
                retail_store_dealer = []
                for dealer in base_dict["retail_store_dealer"]:
                    dealer_mails = []
                    dealer_phones = []
                    for email in dealer["dealer_email"]:
                        dealer_mails.append(RetailStoreDealerEmail(**email))

                    for phone in dealer["dealer_phones"]:
                        dealer_phones.append(RetailStoreDealerPhone(**phone))

                    retail_store_dealer.append(
                        RetailStoreDealer(
                            retail_store_dealer_emails=dealer_mails, retail_store_dealer_phones=dealer_phones
                        )
                    )
                retail_store_tags = []
                for tag in base_dict["retail_store_tags"]:
                    retail_store_tags.append(RetailStoreTag(**tag))

                retail_store_phones = []
                for phone in base_dict["retail_store_phones"]:
                    retail_store_phones.append(RetailStorePhone(**phone))

                retail_store_address = []
                for address in base_dict["retail_store_address"]:
                    retail_store_address.append(RetailStoreAddress(**address))

                base_dict.pop("retail_store_address")
                base_dict.pop("retail_store_phones")
                base_dict.pop("retail_store_tags")
                base_dict.pop("retail_store_dealer")
                return RetailStore(
                    **base_dict,
                    retail_store_tags=retail_store_tags,
                    retail_store_phones=retail_store_phones,
                    retail_store_address=retail_store_address,
                    retail_store_dealer=retail_store_dealer,
                )

            return None

        def filter(
            self,
            social_name: str = None,
            erp_code: str = None,
            business_region: str = None,
            registered_at_partner: str = None,
            mesoregion: str = None,
            microregion: str = None,
            cnpj: str = None,
            cnpj_root: str = None,
            city_council_code: str = None,
            industry_id: str = None,
        ) -> List[RetailStore]:

            params = {
                "social_name": social_name,
                "erp_code": erp_code,
                "business_region": business_region,
                "registered_at_partner": registered_at_partner,
                "mesoregion": mesoregion,
                "microregion": microregion,
                "cnpj": cnpj,
                "cnpj_root": cnpj_root,
                "city_council_code": city_council_code,
                "industry_id": industry_id,
            }
            base_list = self.execute_get(f"{RetailStore.ENDPOINT}/", params)
            base_list = base_list["results"]

            stores = []
            for store in base_list:
                retail_store_dealer = []
                for dealer in store["retail_store_dealer"]:
                    dealer_mails = []
                    dealer_phones = []
                    for email in dealer["dealer_email"]:
                        dealer_mails.append(RetailStoreDealerEmail(**email))

                    for phone in dealer["dealer_phones"]:
                        dealer_phones.append(RetailStoreDealerPhone(**phone))

                    retail_store_dealer.append(
                        RetailStoreDealer(
                            retail_store_dealer_emails=dealer_mails, retail_store_dealer_phones=dealer_phones
                        )
                    )
                retail_store_tags = []
                for tag in store["retail_store_tags"]:
                    retail_store_tags.append(RetailStoreTag(**tag))

                retail_store_phones = []
                for phone in store["retail_store_phones"]:
                    retail_store_phones.append(RetailStorePhone(**phone))

                retail_store_address = []
                for address in store["retail_store_address"]:
                    retail_store_address.append(RetailStoreAddress(**address))

                store.pop("retail_store_address")
                store.pop("retail_store_phones")
                store.pop("retail_store_tags")
                store.pop("retail_store_dealer")
                stores.append(
                    RetailStore(
                        **store,
                        retail_store_tags=retail_store_tags,
                        retail_store_phones=retail_store_phones,
                        retail_store_address=retail_store_address,
                        retail_store_dealer=retail_store_dealer,
                    )
                )

            return stores

        def update(self, retail_store: RetailStore) -> dict:
            base_dict = {
                "id": retail_store.id,
                "social_name": retail_store.social_name,
                "erp_code": retail_store.erp_code,
                "business_region": retail_store.business_region,
                "registered_at_partner": retail_store.registered_at_partner,
                "cnpj": retail_store.cnpj,
                "cnpj_root": retail_store.cnpj_root,
                "industry_id": retail_store.industry_id,
                "direct": retail_store.direct,
                "retail_store_tags": [{"name": t.name} for t in retail_store.retail_store_tags],
                "retail_store_dealer": [],
                "retail_store_phones": [
                    {"value": p["value"], "phone_type": p["phone_type"]} for p in retail_store.retail_store_phones
                ],
                "retail_store_address": [
                    {
                        "address_type": a["address_type"],
                        "city": a["city"],
                        "state_or_province": a["state_or_province"],
                        "street_with_house_number_or_name": a["street_with_house_number_or_name"],
                        "neighborhood": a["neighborhood"],
                        "country": a["country"],
                        "postal_code": a["postal_code"],
                        "mesoregion": a["mesoregion"],
                        "microregion": a["microregion"],
                        "city_council_code": a["city_council_code"],
                    }
                    for a in retail_store.retail_store_address
                ],
            }

            for d in retail_store.retail_store_dealer:
                dealer_dict = {"dealer_email": [], "dealer_phones": []}
                for email in d["retail_store_dealer_emails"]:
                    dealer_dict["dealer_email"].append({"email": email.email})

                for phone in d["retail_store_dealer_phones"]:
                    dealer_dict["dealer_phones"].append({"value": phone["value"], "phone_type": phone["phone_type"]})

                base_dict["retail_store_dealer"].append(dealer_dict)

            return self.execute_put(f"{RetailStore.ENDPOINT}/{retail_store.id}/", base_dict)

        def delete(self) -> None:
            raise NotImplementedError
