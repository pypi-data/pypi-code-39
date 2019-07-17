try:
    from service.ocr.cloud_walk.idcard import IdCard
    from service.ocr.cloud_walk.biz_license import BizLicense
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.ocr.cloud_walk.idcard import IdCard
    from pysubway.service.ocr.cloud_walk.biz_license import BizLicense
