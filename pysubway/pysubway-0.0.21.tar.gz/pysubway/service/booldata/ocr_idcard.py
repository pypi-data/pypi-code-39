import os
from typing import Dict, Any

try:
    from service.booldata.base import BoolDataBase
    from service.booldata.base import CONF
    from service.booldata.base import TEST_ACCOUNT
    from utils.picture import Picture
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.booldata.base import BoolDataBase
    from pysubway.service.booldata.base import CONF
    from pysubway.service.booldata.base import TEST_ACCOUNT
    from pysubway.utils.picture import Picture

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class OCRIdcard(BoolDataBase):
    service = 'ocr_idcard_service'
    mode = 'ocr_idcard_mode'

    @classmethod
    def gen_biz_data(cls, img: str) -> Dict[str, Any]:
        return {
            'service': cls.service,
            'mode': cls.mode,
            'img': img
        }
