try:
    from service import bangsheng
    from service.ocr import cloud_walk
    from service import tonglian
    from service import booldata
    from service import huadao
    from service import suixingfu
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service import bangsheng
    from pysubway.service.ocr import cloud_walk
    from pysubway.service import tonglian
    from pysubway.service import booldata
    from pysubway.service import huadao
    from pysubway.service import suixingfu
