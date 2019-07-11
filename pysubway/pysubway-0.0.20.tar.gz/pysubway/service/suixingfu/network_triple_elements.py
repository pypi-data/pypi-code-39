from typing import Dict

try:
    from service.suixingfu.base import SuixingfuBase
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.suixingfu.base import SuixingfuBase


class NetworkTripleElements(SuixingfuBase):

    def gen_send_data(self, name: str, idcard: str, phone: str, verify_type: str = '05') -> Dict[str, str]:
        return {
            'name': name, 'identNo': idcard, 'phone': phone, 'verifyType': verify_type
        }
