try:
    from service.tonglian.merchant_fraud_blacklist import MerchantFraudBlacklist
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.tonglian.merchant_fraud_blacklist import MerchantFraudBlacklist