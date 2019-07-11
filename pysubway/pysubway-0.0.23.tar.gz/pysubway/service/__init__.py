try:
    from service import bangsheng
    from service.ocr import cloud_walk
    from service import tonglian
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service import bangsheng
    from pysubway.service.ocr import cloud_walk
    from pysubway.service import tonglian