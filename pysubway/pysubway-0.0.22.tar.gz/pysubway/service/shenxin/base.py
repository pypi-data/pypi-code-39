import json
from typing import Dict, Any
from urllib.parse import quote

import requests

try:
    from utils.encryption.aes import AESCrypt
    from utils.encryption.rsa2 import RSAEncryption
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.utils.encryption.aes import AESCrypt
    from pysubway.utils.encryption.rsa2 import RSAEncryption


class ShenxinBase:

    def __init__(self, rsa_prv_key: str, aes_key: str, company_uuid: str, url: str):
        self.rsa_prv_key = rsa_prv_key
        self.aes_key = aes_key
        self.company_uuid = company_uuid
        self.url = url

    @staticmethod
    def sort_dict_value(data_dict: Dict[str, Any]) -> str:
        """
        sort dict value by dict key's order in ascii.
        :param data_dict:
        :return:
        """
        sign_data = ''
        for key in sorted(data_dict.keys()):
            print('key', key)
            value = data_dict[key]
            if isinstance(value, (dict, list)):
                sign_data += json.dumps(data_dict[key], ensure_ascii=False, sort_keys=True).encode('utf-8')
            else:
                sign_data += value
        return sign_data

    @property
    def cls_name(self) -> str:
        return ShenxinBase.__name__

    def gen_request_body(self, send_data: Dict[str, Any]) -> str:
        aes_cipher = AESCrypt(self.aes_key)
        s1 = json.dumps(send_data)
        encrypt_biz_data = aes_cipher.encrypt(s1)
        return quote(encrypt_biz_data, safe='')

    def gen_sign(self, send_data: Dict[str, Any]) -> str:
        sorted_biz_data = self.sort_dict_value(send_data)
        sign = RSAEncryption.gen_signature(sorted_biz_data, self.rsa_prv_key)
        return quote(sign, safe='')

    def request(self, send_data: Dict[str, Any]) -> Dict[str, Any]:
        res = requests.post(self.url, json=send_data)
        if not res.ok:
            raise ValueError(f'res.text {res.text} res.status_code {res.status_code} is invalid')
        return res.json()
