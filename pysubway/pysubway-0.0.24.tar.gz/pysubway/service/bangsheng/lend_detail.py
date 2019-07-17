try:
    from service.bangsheng.base import BangShengBase
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.bangsheng.base import BangShengBase

class LendDetail(BangShengBase):
    uri = '/v1/person/loan/lend-detail/t2'
