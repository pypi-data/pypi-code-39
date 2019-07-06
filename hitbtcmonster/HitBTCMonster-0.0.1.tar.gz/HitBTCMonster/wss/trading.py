from .core import (
    rand, serialize
)


class Trading:

    def __init__(self, core):
        self.CORE = core

    def subscribe_reports(self, status, **params) -> int:
        method = 'subscribeReports'
        rid = rand()
        if status is False:
            method = 'un' + method

        self.CORE.send(method, rid, **params)
        return rid

    def place(self, **params) -> int:
        rid = rand()
        params = {
            'type': params.get('_TYPE', None),
            'price': params.get('PRICE', None),
            'symbol': params.get('SYMBOL', None),
            'side': params.get('TYPE', '').lower(),
            'clientOrderId': params.get('CID', None),
            'quantity': params.get('QUANTITY', None),
            'postOnly': params.get('POST_ONLY', None),
            'stopPrice': params.get('STOP_PRICE', None),
            'expireTime': params.get('EXPIRE_TIME', None),
            'timeInForce': params.get('TIME_IN_FORCE', None),
            'strictValidate': params.get('STRICT_VALIDATE', None)
        }
        params = serialize(params)
        self.CORE.send('newOrder', rid, **params)
        return rid

    def cancel(self, **params) -> int:
        rid = rand()
        params = {
            'clientOrderId': params.get('CID', None)
        }
        params = serialize(params)
        self.CORE.send('cancelOrder', rid, **params)
        return rid

    def replace(self, **params) -> int:
        rid = rand()
        params = {
            'price': params.get('PRICE', None),
            'quantity': params.get('QUANTITY', None),
            'clientOrderId': params.get('CID', None),
            'requestClientId': params.get('_CID', None)
        }
        params = serialize(params)
        self.CORE.send('cancelReplaceOrder', rid, **params)
        return rid

    def get_orders(self, **params) -> int:
        rid = rand()
        self.CORE.send('getOrders', rid, **params)
        return rid

    def get_trading_balance(self, **params) -> int:
        rid = rand()
        self.CORE.send('getTradingBalance', rid, **params)
        return rid
