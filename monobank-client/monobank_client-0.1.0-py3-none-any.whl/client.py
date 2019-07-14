import datetime as dt
from abc import abstractmethod
from typing import Union, List

from . import utils
from .settings import (MONOBANK_API_CURRENCY_ENDPOINT,
                       MONOBANK_API_CLIENT_INFO_ENDPOINT,
                       MONOBANK_API_STATEMENTS_ENDPOINT)


Time = Union[int, str, dt.datetime]


class ClientBase:

    @abstractmethod
    def _get_headers(self) -> dict:
        pass

    @staticmethod
    def get_currency() -> List[dict]:
        return utils.json_request(url=MONOBANK_API_CURRENCY_ENDPOINT)

    def get_client_info(self) -> dict:
        return utils.json_request(url=MONOBANK_API_CLIENT_INFO_ENDPOINT, headers=self._get_headers())

    def get_statements(self, account: str, from_time: Time, to_time: Time = '') -> List[dict]:
        if isinstance(from_time, dt.datetime):
            from_time = from_time.timestamp()
        if isinstance(to_time, dt.datetime):
            to_time = to_time.timestamp()

        url = MONOBANK_API_STATEMENTS_ENDPOINT.format(account=account, from_timestamp=from_time, to_timestamp=to_time)
        return utils.json_request(url=url, headers=self._get_headers())


class PersonalClient(ClientBase):

    def __init__(self, token):
        self.token = token

    def _get_headers(self) -> dict:
        return {'X-Token': self.token}
