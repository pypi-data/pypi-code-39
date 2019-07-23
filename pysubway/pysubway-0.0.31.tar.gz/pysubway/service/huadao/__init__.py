import json
from json.decoder import JSONDecodeError
from typing import Dict
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

try:
    from utils import udict
except (ModuleNotFoundError, ImportError) as e:
    from pysubway.utils import udict


class HuaDaoBase:
    """
    华道返回 xml
    """
    url_access_token = 'http://opensdk.emay.cn:9080/HD_GetAccess_Token.asmx/GetACCESS_TOKEN'

    def __init__(self, token: str):
        self.token: str = token
        self.full_url: str = ''
        self.biz_data: Dict = dict()

    @classmethod
    def get_token(cls, AppID: str, AppSecret: str, Key: str) -> str:
        full_url = '?'.join((cls.url_access_token, urlencode({
            'AppID': AppID,
            'AppSecret': AppSecret,
            'Key': Key
        })))
        r = requests.get(full_url)
        return r.text

    @staticmethod
    def generate_full_url(url: str, biz_data: Dict[str, str]) -> str:
        """
        you can get full_url by this function return
        :param url: base url
        :param biz_data:
        :return:
        """
        return '?'.join((url, urlencode(biz_data)))

    def set_full_url(self, url: str, biz_data: Dict[str, str]) -> 'HuaDaoBase':
        self.full_url = self.generate_full_url(url, biz_data)
        return self

    def request(self, full_url: str = '') -> Dict[str, str]:
        full_url = full_url or self.full_url
        r = requests.get(full_url)
        if r.ok:
            try:
                bs = BeautifulSoup(r.text, features='html.parser')
                return json.loads(bs.text)
            except JSONDecodeError as e:
                raise TypeError(f'JSONDecodeError, raw resp {r.text}')
            except Exception as e:
                raise SystemError(f'raw resp1 {r.text}')
        else:
            raise ValueError(f'raw resp2 {r.text}')


class BankFiveElements(HuaDaoBase):
    url = 'http://opensdk.emay.cn:9099/SF_YZ_API/SFService.asmx/Get_EMW_GetBank_Card_Five_RZ'

    def set_biz_data(self, name: str = '', idcard: str = '', cardNo: str = '', phone: str = '',
                     bankAccountType: str = '') -> 'BankFiveElements':
        self.biz_data = udict.Dict.filter(locals())
        self.biz_data['ACCESS_TOKEN'] = self.token
        return self
