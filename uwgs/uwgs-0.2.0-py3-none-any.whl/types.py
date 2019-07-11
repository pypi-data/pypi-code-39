import requests
import json
from collections import namedtuple


class Payload:
    def __init__(self, resp: requests.Response):
        self._status_code: int = resp.status_code
        self._data: dict = json.loads(resp.text)

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def ok(self) -> bool:
        return 200 <= self._status_code and 300 > self._status_code

    @property
    def data(self) -> dict:
        return self._data

    def __repr__(self) -> str:
        return json.dumps({
            'status_code': self._status_code,
            'ok': self.ok,
            'data': self.data})

def default_get_headers() -> dict:
    return {
        "accept": "application/json"
    }

def get_headers(**kwargs: dict) -> dict:
    h = default_get_headers()
    for k, v in kwargs.items():
        if v:
            h[k] = v
    return h

MemberLookup = namedtuple('MemberLookup', ['group_id', 'member_id'])
