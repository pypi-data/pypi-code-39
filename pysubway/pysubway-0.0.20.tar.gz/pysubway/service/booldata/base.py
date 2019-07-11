import json
from typing import Dict, Any, Optional

import requests

try:
    from utils import udict
    from utils.encryption.aes import AESCrypt
    from utils.encryption.rsa2 import RSAEncryption
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.utils import udict
    from pysubway.utils.encryption.aes import AESCrypt
    from pysubway.utils.encryption.rsa2 import RSAEncryption


class BoolDataBase:
    urls = {
        'local': 'http://localhost:8000/api/lightning/product/query',
        'sit': 'http://guard.shouxin168.net/api/lightning/product/query',
        'prod': 'https://guard.shouxin168.com/api/lightning/product/query'
    }

    def __init__(self, rsa_prv_key: str, aes_key: str, company_uuid: str, url: str = ''):
        self.url = url or self.urls['prod']
        print(f'use url {self.url}')
        self.rsa_prv_key = rsa_prv_key
        self.aes_key = aes_key
        self.company_uuid = company_uuid
        self.resp_data = None
        self.biz_data = None

    @classmethod
    def gen_biz_data(cls, *args) -> Dict[str, Any]:
        raise NotImplementedError()

    def encrypt_biz_data(self, biz_data: Dict[str, str]) -> str:
        sorted_str = json.dumps(biz_data, sort_keys=True)
        return AESCrypt(self.aes_key).encrypt(sorted_str)

    def gen_sign(self, biz_data: Dict[str, str]) -> str:
        sorted_str = udict.Dict(biz_data).sort_keys()
        return RSAEncryption.gen_signature(sorted_str, self.rsa_prv_key)

    def request(self, biz_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        biz_data = biz_data or self.biz_data
        data = {
            'sign': self.gen_sign(biz_data),
            'biz_data': self.encrypt_biz_data(biz_data),
            'institution_id': self.company_uuid,
        }
        resp = requests.post(self.url, data=data)
        if resp.ok:
            self.resp_data = resp.json()
            return self.resp_data
        else:
            raise ValueError(resp.text)

    @staticmethod
    def is_success_request(resp: Dict[str, Any]) -> bool:
        if isinstance(resp, dict) and resp.get('resp_code') == 'SW0000':
            return True
        else:
            print(resp)
            return False

    def is_succeed(self, resp: Dict[str, Any] = None) -> bool:
        """
        the function is same to is_success_request,
        but support to chain operate
        :param resp:
        :return:
        """
        response = self.resp_data if resp is None else resp
        return self.is_success_request(response)
