import hashlib
from collections import OrderedDict
from typing import Dict, Any, Callable, Optional

import requests

try:
    from utils.ustring import to_bytes
    from utils.utime import timestamp
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.utils.ustring import to_bytes
    from pysubway.utils.utime import timestamp


class ShanghaishuheBase:
    url = 'http://auth.shuhe360.cn:8801/auth/auth-core'
    auth_elements = {
        # 银行卡三要素
        'bankcard_triple_eles': "1101",
        # 银行卡四要素
        'bankcard_four_eles': "1111",
        # 运营商三要素
        'network_triple_eles': "1110",
        # 银行卡三要素详版
        'bankcard_triple_eles_detail': "1101#L",
        # 银行卡四要素详版
        'bankcard_four_eles_detail': "1111#L",
        # 身份二要素认证
        'idcard_two_eles': "1100",
    }
    unsigned_data_order = 'accountName|authElement|bankCardNo|idCardNo|idCardType|phoneNo|expired|cvn2|serialNo|userName|accountPassword'.split(
        '|')

    def __init__(self, account_name: str, account_pwd: str, url: str, version: str = '01'):
        self.url = url
        self.account_name = account_name
        self.account_pwd = account_pwd
        self.version = version
        self.send_data = None

    def gen_send_data(self, **kwargs) -> Dict[str, str]:
        raise NotImplementedError()

    def set_send_data(self, **kwargs) -> 'ShanghaishuheBase':
        self.send_data = self.gen_send_data(**kwargs)
        return self

    @classmethod
    def fmt_func_bak(cls, data: Dict[str, Any]):
        result = OrderedDict()
        for i in cls.unsigned_data_order:
            result[i] = str(data[i]) if i in data else ''
        return '|'.join(result.values())

    @staticmethod
    def fmt_func(accountName='', authElement='', bankCardNo='', idCardNo='', idCardType='', phoneNo='', expired='',
                 cvn2='', serialNo='', userName='', accountPassword=''):
        """
        committed by xiazhi, it's great
        :return:
        """
        return "|".join((accountName, authElement, bankCardNo, idCardNo, idCardType, phoneNo, expired,
                         cvn2, serialNo, userName, accountPassword))

    def gen_sign(self, data: Dict[str, str], fmt_func: Callable = None) -> str:
        """
        签名值为：
        SHA1(accountName|authElement|bankCardNo|idCardNo|idCardType|phoneNo|expired|cvn2|serialNo|userName|accountPassword)组合后的字符串通过SHA1摘要（大写），如无数据则
        采用||中间不留空。
        SHA1的计算小工具可参考：https://1024tools.com/hash
        :param data:
        :param fmt_func:
        :return:
        """
        data['accountPassword'] = self.account_pwd
        fmted = fmt_func(data) if fmt_func else self.fmt_func_bak(data)
        print(fmted)
        return hashlib.sha1(to_bytes(fmted)).hexdigest().upper()

    def request(self, send_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        send_data = send_data or self.send_data
        print('send_data', send_data)
        response = requests.post(self.url, json=send_data)
        if response.ok:
            return response.json()
        raise SystemError(f'response {response.text}')


class BankcardFourEles(ShanghaishuheBase):

    def gen_send_data(self, idCardNo: str = '', userName: str = '', bankCardNo: str = '', phoneNo: str = '',
                      idCardType='01') -> Dict[str, str]:
        kwargs = {k: v for k, v in locals().items() if k not in ('self', 'cls')}
        print('kwargs', kwargs)
        if '' in kwargs.values():
            raise ValueError(f"invalid args kwargs {kwargs}")
        kwargs.update({
            'authElement': self.auth_elements['bankcard_four_eles'],
            'accountName': self.account_name,
            'serialNo': timestamp(precision='ms'),
            'version': self.version,
        })
        sign = self.gen_sign(kwargs)
        kwargs['sign'] = sign
        self.send_data = kwargs
        return kwargs


if __name__ == '__main__':
    from service.shanghaishuhe.gitignore import SHANGHAI_SHUHE_ACCOUNT_INFO

    s = BankcardFourEles(SHANGHAI_SHUHE_ACCOUNT_INFO['account_name'], SHANGHAI_SHUHE_ACCOUNT_INFO['account_pwd'],
                         BankcardFourEles.url).set_send_data(idCardNo='**', userName='**',
                                                             bankCardNo='**', phoneNo='**',
                                                             idCardType='**').request()
    print(s)
