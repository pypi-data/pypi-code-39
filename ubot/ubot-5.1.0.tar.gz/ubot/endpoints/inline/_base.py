from abc import ABC, ABCMeta

from .._mixins import ReplyMarkup
from ..._utils.casing import camel_to_snake
from ..._utils.random import random_string


class InlineQueryResultMixin(ABC):
    __slots__ = []
    _type: str
    prefix: str
    args: dict


class InlineQueryResult(ReplyMarkup, metaclass=ABCMeta):
    __slots__ = ['_type', 'prefix', 'args']

    def __init__(self):
        classname = self.__class__.__name__
        self._type = camel_to_snake(classname)
        self.prefix = self._type

        self.args = {
            'type': self._type,
            'id': random_string(8)
        }


class InlineQueryResultFile(InlineQueryResult, metaclass=ABCMeta):
    def __init__(self, url, thumb_url):
        super().__init__()
        url_key = f'{self.prefix}_url'
        self.args[url_key] = url
        self.args['thumb_url'] = thumb_url


class InlineQueryResultCachedFile(InlineQueryResult, metaclass=ABCMeta):
    def __init_(self, file_id):
        super().__init__()
        self._type = self._type[8:]  # "cached_"
        file_id_key = f'{self.prefix}_file_id'
        self.args[file_id_key] = file_id


class InputMessageContent(ABC):
    __slots__ = ['args']
