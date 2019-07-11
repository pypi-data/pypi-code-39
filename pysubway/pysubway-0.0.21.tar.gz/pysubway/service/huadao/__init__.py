import json
from json.decoder import JSONDecodeError
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup


class HuaDao:
    """
    华道返回 xml
    """

    @staticmethod
    def get_token(AppID, AppSecret, Key):
        access_token = 'http://opensdk.emay.cn:9080/HD_GetAccess_Token.asmx/GetACCESS_TOKEN'
        full_url = '?'.join((access_token, urlencode({
            'AppID': AppID,
            'AppSecret': AppSecret,
            'Key': Key
        })))
        r = requests.get(full_url)
        return r.text

    @staticmethod
    def gen_full_url(url, biz_data):
        """
        you can get full_url by this function return
        :param url: base url
        :param biz_data:
        :return:
        """
        return '?'.join((url, urlencode(biz_data)))

    @classmethod
    def _request(cls, url, biz_data):
        full_url = cls.gen_full_url(url, biz_data)
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


class BankFiveElements(HuaDao):
    url = 'http://opensdk.emay.cn:9099/SF_YZ_API/SFService.asmx/Get_EMW_GetBank_Card_Five_RZ'

    def __init__(self, name, idcard, cardNo, phone, bankAccountType, token):
        self.token = token
        self.biz_data = {
            'name': name,
            'idcard': idcard,
            'cardNo': cardNo,
            'phone': phone,
            'bankAccountType': bankAccountType,
            'ACCESS_TOKEN': self.token
        }

    def request(self):
        return self._request(self.url, self.biz_data)


if __name__ == '__main__':
    a1 = BankFiveElements('a', 'b', 'c', 'd', 'f', '')
    a1.request()
