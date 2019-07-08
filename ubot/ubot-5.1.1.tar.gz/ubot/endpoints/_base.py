from abc import ABC

from .._utils.case_insensitive_dict import CaseInsensitiveDict
from ..bot import BotRequest


class BaseMixin(ABC):
    __slots__ = []
    args: dict


# unused currently
class EndpointMixin(ABC):
    method: str
    endpoint: str
    args: dict
    data: bytes or None
    headers: CaseInsensitiveDict


class Endpoint(ABC):
    __slots__ = ['method', 'endpoints', 'args', 'data', 'headers']

    def __init__(self):
        self.method = 'GET'
        classname = self.__class__.__name__
        self.endpoint = f'{classname[0].lower()}{classname[1:]}'

        self.args = {}
        self.data = None
        self.headers = CaseInsensitiveDict()

    def serialize(self):
        return BotRequest(
            method=self.method,
            endpoint=self.endpoint,
            params=self.args,
            data=self.data,
            headers=self.headers
        )
