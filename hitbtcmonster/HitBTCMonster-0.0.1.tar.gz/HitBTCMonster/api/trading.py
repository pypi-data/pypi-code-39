import datetime
from .core import serialize


class Trading:

    def __init__(self, core):
        self.CORE = core

    def get_orders(self, required: bool = False, **params) -> dict or list:
        _params = {
            'till': params.get('TILL', ''),
            'limit': params.get('LIMIT', 100),
            'offset': params.get('OFFSET', ''),
            'symbol': params.get('SYMBOL', ''),
            'clientOrderId': params.get('CID', ''),
            'from': params.get('FROM', (datetime.datetime.today() - datetime.timedelta(3 * 365 / 12)).isoformat() + 'Z')
        }
        while True:
            data = self.CORE.send('GET', 'history/order', params={**_params})
            serialized = serialize(required=required, data=data)
            if serialized is not None:
                return data

    def get_transactions_history(self, required: bool = False, **params) -> dict or list:
        _params = {
            'id': params.get('ID', ''),
            'by': params.get('BY', ''),
            'sort': params.get('SORT', ''),
            'till': params.get('TILL', ''),
            'limit': params.get('LIMIT', 100),
            'offset': params.get('OFFSET', ''),
            'symbol': params.get('SYMBOL', ''),
            'currency': params.get('CURRENCY', ''),
            'from': params.get('FROM', (datetime.datetime.today() - datetime.timedelta(3 * 365 / 12)).isoformat() + 'Z')
        }
        while True:
            data = self.CORE.send('GET', 'account/transactions/{ID}'.format(
                ID=params.get('ID', '')
            ), params={**_params})

            serialized = serialize(required=required, data=data)
            if serialized is not None:
                return data

    def get_trades(self, required: bool = False, **params) -> dict or list:
        _params = {
            'by': params.get('BY', ''),
            'sort': params.get('SORT', ''),
            'till': params.get('TILL', ''),
            'limit': params.get('LIMIT', 100),
            'offset': params.get('OFFSET', ''),
            'symbol': params.get('SYMBOL', ''),
            'from': params.get('FROM', (datetime.datetime.today() - datetime.timedelta(3 * 365 / 12)).isoformat() + 'Z')
        }
        while True:
            data = self.CORE.send('GET', 'history/order', params={**_params})

            serialized = serialize(required=required, data=data)
            if serialized is not None:
                return data

    def get_active_orders(self, required: bool = False, **params) -> dict or list:
        _params = {
            'wait': params.get('WAIT', ''),
            'symbol': params.get('SYMBOL', '')
        }
        while True:
            data = self.CORE.send('GET', 'order/{CID}'.format(
                CID=params.get('CID', '')
            ), params={**_params})

            serialized = serialize(required=required, data=data)
            if serialized is not None:
                return data

    def get_trading_balance(self, required: bool = False, **params):
        while True:
            data = self.CORE.send('GET', 'trading/balance')

            serialized = serialize(required=required, data=data)
            if serialized is not None:
                if isinstance(data, dict):
                    error = data.get('error', None)
                else:
                    error = None
                if error is None:
                    for trading_balance in data:
                        if trading_balance.get('CURRENCY') == params.get('CURRENCY', ''):
                            return trading_balance
                return data

    def place(self, required: bool = False, **params):
        _params = {
            'type': params.get('_TYPE', ''),
            'price': params.get('PRICE', ''),
            'symbol': params.get('SYMBOL', ''),
            'quantity': params.get('QUANTITY', ''),
            'side': params.get('TYPE', '').lower(),
            'postOnly': params.get('POST_ONLY', ''),
            'stopPrice': params.get('STOP_PRICE', ''),
            'expireTime': params.get('EXPIRE_TIME', ''),
            'timeInForce': params.get('TIME_IN_FORCE', ''),
            'strictValidate': params.get('STRICT_VALIDATE', '')
        }
        while True:
            data = self.CORE.send('POST', 'order', params={**_params})

            serialized = serialize(required=required, data=data)
            if serialized is not None:
                return data

    def replace(self, required: bool = False, **params):
        _params = {
            'PRICE': params.get('PRICE', ''),
            'QUANTITY': params.get('QUANTITY', '')
        }
        while True:
            i_response = self.get_active_orders(required=required, CID=params.get('CID', ''))
            if isinstance(i_response, dict):
                i_error = i_response.get('error', None)
            else:
                i_error = None
            if i_error is True:
                return i_response
            _params.update({
                'TYPE': i_response.get('TYPE', ''),
                'SYMBOL': i_response.get('SYMBOL', '')
            })
            c_response = self.cancel(required=required, CID=params.get('CID', ''))
            if isinstance(c_response, dict):
                c_error = c_response.get('error', None)
            else:
                c_error = None
            if c_error is True:
                return c_response
            response = self.place(required=required, **_params)
            return response

    def cancel(self, required: bool = False, **params):
        _params = {
            'symbol': params.get('SYMBOL', '')
        }
        while True:
            data = self.CORE.send('DELETE', 'order/{CID}'.format(
                CID=params.get('CID', '')
            ), params={**_params})

            serialized = serialize(required=required, data=data)
            if serialized is not None:
                return data
