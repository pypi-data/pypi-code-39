import os
from typing import Dict, Any

try:
    from service.booldata.base import BoolDataBase
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.booldata.base import BoolDataBase

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class Bankcard5Eles(BoolDataBase):
    service = 'bankcard_five_elements_service'
    mode = 'bankcard_five_elements_mode'

    @classmethod
    def gen_biz_data(cls, name: str, ident_number: str, bankcard: str, phone: str, account_type='1') -> Dict[str, Any]:
        return {
            "name": name,
            "ident_number": ident_number,
            "bankcard": bankcard,
            "account_type": account_type,
            "phone": phone,
            "service": cls.service,
            "mode": cls.mode
        }

    def set_biz_data(self, name: str, ident_number: str, bankcard: str, phone: str, account_type='1') -> BoolDataBase:
        """
        support, Bankcard5Eles().set_biz_data().request()
        :param name:
        :param ident_number:
        :param bankcard:
        :param phone:
        :param account_type:
        :return:
        """
        self.biz_data = self.gen_biz_data(name, ident_number, bankcard, phone, account_type=account_type)
        return self


if __name__ == '__main__':
    from service.booldata.gitignore import TEST_ACCOUNT

    s = Bankcard5Eles(TEST_ACCOUNT['rsa_prv_key'], TEST_ACCOUNT['aes_key'], TEST_ACCOUNT['company_uuid'],
                      Bankcard5Eles.urls['prod']).set_biz_data('**', '**',
                                                               '**', '**').request()
    list.count()
    print(s)
