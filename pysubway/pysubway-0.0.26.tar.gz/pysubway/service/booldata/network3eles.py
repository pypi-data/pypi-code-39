from typing import Dict, Any

import pandas as pd

try:
    from service.booldata.base import BoolDataBase
    from utils import udict
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.booldata.base import BoolDataBase
    from pysubway.utils import udict


class Network3Eles(BoolDataBase):
    service = 'network_operator_triple_elements'
    mode = 'mode_triple_elements'
    default_part = {
        'name': '',
        'phone': '',
        'idcard': ''
    }

    @classmethod
    def generate_biz_data(cls, name: str, phone: str, ident_number: str) -> Dict[str, Any]:
        biz_data = udict.Dict.filter(locals())
        biz_data.update({
            "service": cls.service,
            "mode": cls.mode
        })
        return biz_data

    def set_biz_data(self, name: str, phone: str, ident_number: str) -> 'Network3Eles':
        self.biz_data = self.generate_biz_data(name, phone, ident_number)
        return self

    def result_as_df_partial(self, append_biz_data: bool = True) -> pd.DataFrame:
        return self.result_as_df(self.response.get('resp_data', {}), self.default_part,
                                 append_biz_data=append_biz_data)


if __name__ == '__main__':
    from gitignore import BOOLDATA_ACCOUNT, booldata_personal_law

    print('test result_as_df_partial start ...')
    data = booldata_personal_law(3)
    name = data['name']
    phone = data['phone']
    idcard = data['id_num']
    law_list = Network3Eles(BOOLDATA_ACCOUNT['rsa_prv_key'], BOOLDATA_ACCOUNT['aes_key'],
                            BOOLDATA_ACCOUNT['company_uuid'])
    law_list.set_biz_data(name, phone, idcard).request()
    s = law_list.result_as_df_partial()
    print(s)
    print('test result_as_df_partial end ...')
