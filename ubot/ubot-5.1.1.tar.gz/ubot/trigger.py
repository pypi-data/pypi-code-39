from abc import ABC, abstractmethod

from .bot import Bot


class Trigger(ABC):
    __slots__ = []

    @classmethod
    @abstractmethod
    async def match(cls, update, bot: Bot):
        """Returns a truthy value if update matches, a falsy value if it doesn't. Async supported."""
        pass

    @classmethod
    @abstractmethod
    async def handle(cls, update, bot: Bot):
        pass
