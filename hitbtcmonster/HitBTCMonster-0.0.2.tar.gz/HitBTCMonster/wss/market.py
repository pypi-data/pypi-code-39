from .core import (
    rand, serialize
)


class Market:

    def __init__(self, core):
        self.CORE = core

    def get_currencies(self, **params) -> int:
        rid = rand()
        params = {
            'currency': params.get('CURRENCY', None)
        }
        params = serialize(params)
        currency = params.get('CURRENCY', None)
        if currency:
            method = 'getCurrency'
        else:
            method = 'getCurrencies'
        self.CORE.CONNECTION.send(method, rid, **params)
        return rid

    def get_symbols(self, **params) -> int:
        rid = rand()
        params = {
            'symbol': params.get('SYMBOL', None)
        }
        params = serialize(params)
        symbol = params.get('SYMBOL', None)
        if symbol:
            method = 'getSymbol'
        else:
            method = 'getSymbols'

        self.CORE.send(method, rid, **params)
        return rid

    def get_trades(self, **params) -> int:
        rid = rand()
        params = {
            'by': params.get('BY', None),
            'sort': params.get('SORT', None),
            'from': params.get('FROM', None),
            'till': params.get('TILL', None),
            'limit': params.get('LIMIT', None),
            'offset': params.get('OFFSET', None),
            'symbol': params.get('SYMBOL', None)
        }
        params = serialize(params)
        self.CORE.send('getTrades', rid, **params)
        return rid

    def subscribe_trades(self, status, **params) -> int:
        method = 'subscribeTrades'
        rid = rand()
        if status is False:
            method = 'un' + method

        self.CORE.send(method, rid, **params)
        return rid

    def subscribe_tickers(self, status, **params) -> int:
        method = 'subscribeTicker'
        rid = rand()
        if status is False:
            method = 'un' + method

        self.CORE.send(method, rid, **params)
        return rid

    def subscribe_orderbook(self, status, **params) -> int:
        method = 'subscribeOrderbook'
        rid = rand()
        if status is False:
            method = 'un' + method

        self.CORE.send(method, rid, **params)
        return rid

    def subscribe_candles(self, status, **params) -> int:
        method = 'subscribeCandles'
        rid = rand()
        if status is False:
            method = 'un' + method

        self.CORE.send(method, rid, **params)
        return rid
