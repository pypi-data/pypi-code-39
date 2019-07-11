from typing import Dict

try:
    from service.suixingfu.base import SuixingfuBase
except Exception as e:
    from pysubway.service.suixingfu.base import SuixingfuBase


class BankcardTripleElements(SuixingfuBase):

    def gen_send_data(self, name: str, idcard: str, bankcard: str, verify_type: str = '03') -> Dict[str, str]:
        return {
            'name': name, 'identNo': idcard, 'cardNo': bankcard, 'verifyType': verify_type
        }
