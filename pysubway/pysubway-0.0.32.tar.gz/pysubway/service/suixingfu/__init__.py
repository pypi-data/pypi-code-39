try:
    from service.suixingfu.bankcard_four_elements import BankcardFourElements
    from service.suixingfu.bankcard_triple_elements import BankcardTripleElements
    from service.suixingfu.merchant_fraud_blacklist import MerchantFraudBlacklist
    from service.suixingfu.network_triple_elements import NetworkTripleElements
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.suixingfu.bankcard_four_elements import BankcardFourElements
    from pysubway.service.suixingfu.bankcard_triple_elements import BankcardTripleElements
    from pysubway.service.suixingfu.merchant_fraud_blacklist import MerchantFraudBlacklist
    from pysubway.service.suixingfu.network_triple_elements import NetworkTripleElements