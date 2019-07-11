from hashlib import sha256
from hmac import new as new_hmac
from json import (
    dumps, loads
)
from random import randint
from time import time

from websocket import create_connection


def rand():
    return int(randint(1, 9999999999999999) * time())


def serialize(params):
    return {
        _key: _value for _key, _value in params.items() if _value is not None and _value
    }


class HitBTC:

    def __init__(self, public: str, secret: str, gateway: str = None):
        self.PUBLIC = public
        self.SECRET = secret
        self.GATEWAY = gateway or 'wss://api.hitbtc.com/api/2/ws'
        self.CONNECTION = create_connection(self.GATEWAY)

        self.authenticate()

    def connect(self):
        self.CONNECTION.connect(self.GATEWAY)

    def disconnect(self):
        self.CONNECTION.close()

    def send(self, method: str, rid: float = None, **params) -> int:
        if self.CONNECTION.connected:
            payload = {
                'method': method,
                'params': params,
                'id': rid or int(10000 * time())
            }
            payload = dumps(payload)
            return self.CONNECTION.send(payload)

    def receive(self) -> dict:
        try:
            response = loads(self.CONNECTION.recv())
            if isinstance(response, dict):
                error = response.get('error', None)
                if error:
                    error.update({
                        'error': True,
                        'id': response.get('id'),
                        'jsonrpc': response.get('jsonrpc'),
                    })
                    return error
            return response
        except Exception as error:
            return {
                'error': True,
                'message': error
            }

    def authenticate(self, basic: bool = True, custom_nonce: str = None):
        if basic:
            algorithm = 'BASIC'
            secret = self.SECRET
            params = {'sKey': secret}
        else:
            algorithm = 'HS256'
            nonce = custom_nonce or str(round(time() * 91010109))
            raw_sig = (self.PUBLIC + nonce).encode(encoding='UTF-8')
            signature = new_hmac(self.SECRET, raw_sig, sha256).hexdigest()
            params = {'nonce': nonce, 'signature': signature}

        params.update(
            {
                'algo': algorithm,
                'pKey': self.PUBLIC
            }
        )

        self.send('login', **params)
