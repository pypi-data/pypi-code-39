try:
    from service.bangsheng.base import BangShengBase
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.bangsheng.base import BangShengBase

class OverdueDetail(BangShengBase):
    uri = '/v1/person/loan/overdue-detail/t2'
