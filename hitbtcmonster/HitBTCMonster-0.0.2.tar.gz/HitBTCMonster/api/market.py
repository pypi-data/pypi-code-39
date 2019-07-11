from .core import serialize


class Market:

    def __init__(self, core):
        self.CORE = core

    def get_currencies(self, required: bool = False, **params) -> dict or list:
        while True:
            data = self.CORE.send('get', 'public/currency/{CURRENCY}'.format(
                CURRENCY=params.get('CURRENCY', '')
            ))
            serialized = serialize(required=required, data=data)
            if serialized is not None:
                return data

    def get_symbols(self, required: bool = False, **params) -> dict or list:
        while True:
            data = self.CORE.send('get', 'public/symbol/{SYMBOL}'.format(
                SYMBOL=params.get('SYMBOL', '')
            ))
            serialized = serialize(required=required, data=data)
            if serialized is not None:
                return data

    def get_trades(self, required: bool = False, **params) -> dict or list:
        _params = {
            'by': params.get('BY', ''),
            'sort': params.get('SORT', ''),
            'from': params.get('FROM', ''),
            'till': params.get('TILL', ''),
            'limit': params.get('LIMIT', 100),
            'offset': params.get('OFFSET', ''),
        }
        while True:
            data = self.CORE.send('get', 'public/trades/{SYMBOL}'.format(
                SYMBOL=params.get('SYMBOL', '')
            ), params={**_params})
            serialized = serialize(required=required, data=data)
            if serialized is not None:
                return data

    def get_tickers(self, required: bool = False, **params) -> dict or list:
        while True:
            data = self.CORE.send('get', 'public/ticker/{SYMBOL}'.format(
                SYMBOL=params.get('SYMBOL', '')
            ))
            serialized = serialize(required=required, data=data)
            if serialized is not None:
                return data

    def get_orderbook(self, required: bool = False, **params) -> dict or list:
        _params = {
            'limit': params.get('LIMIT', 100),
        }
        while True:
            data = self.CORE.send('get', 'public/orderbook/{SYMBOL}'.format(
                SYMBOL=params.get('SYMBOL', '')
            ), params={**_params})
            serialized = serialize(required=required, data=data)
            if serialized is not None:
                return data

    def get_candles(self, required: bool = False, **params) -> dict or list:
        _params = {
            'sort': params.get('SORT', ''),
            'from': params.get('FROM', ''),
            'till': params.get('TILL', ''),
            'limit': params.get('LIMIT', 100),
            'offset': params.get('OFFSET', ''),
            'period': params.get('PERIOD', 'M1'),
        }
        while True:
            data = self.CORE.send('get', 'public/candles/{SYMBOL}'.format(
                SYMBOL=params.get('SYMBOL', '')
            ), params={**_params})
            serialized = serialize(required=required, data=data)
            if serialized is not None:
                return data
