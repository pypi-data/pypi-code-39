try:
    from service.bangsheng.base import BangShengBase
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.bangsheng.base import BangShengBase

class LoanRisk(BangShengBase):
    uri = '/v1/person/loan/risk'
