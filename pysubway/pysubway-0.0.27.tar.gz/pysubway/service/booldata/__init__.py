try:
    from service.booldata.bankcard5eles import Bankcard5Eles
    from service.booldata.ocr_idcard import OCRIdcard
    from service.booldata.hz_risk_model import HzRiskModel
except (ModuleNotFoundError, ImportError) as e:
    from pysubway.service.booldata.bankcard5eles import Bankcard5Eles
    from pysubway.service.booldata.ocr_idcard import OCRIdcard
    from pysubway.service.booldata.hz_risk_model import HzRiskModel