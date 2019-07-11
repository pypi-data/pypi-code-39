from typing import Dict

try:
    from service.suixingfu.base import SuixingfuBase
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.suixingfu.base import SuixingfuBase


class BankcardFourElements(SuixingfuBase):

    def gen_send_data(self, name: str, idcard: str, bankcard: str, phone: str, verify_type: str = '04') -> Dict[
        str, str]:
        return {
            'name': name, 'identNo': idcard, 'cardNo': bankcard, 'verifyType': verify_type, 'phone': phone
        }
