try:
    from service.shenxin.bankcard_five_elements import BankcardFiveElements
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.shenxin.bankcard_five_elements import BankcardFiveElements
