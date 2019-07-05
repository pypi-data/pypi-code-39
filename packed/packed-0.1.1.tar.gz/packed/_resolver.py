from collections import OrderedDict
from typing import Any, Dict, Optional, Type

__all__ = ("Resolver",)


AnyClass = Type[Any]


class Resolver:
    def __init__(self) -> None:
        self._registry = OrderedDict()  # type: Dict[str, AnyClass]

    def register(self, cls: AnyClass, name: Optional[str] = None) -> None:
        if name is None:
            name = cls.__name__
        if name in self._registry:
            raise KeyError(name)
        self._registry[name] = cls

    def resolve_type(self, name: str) -> AnyClass:
        if name not in self._registry:
            raise KeyError(name)
        return self._registry[name]

    def resolve_name(self, cls: AnyClass) -> str:
        for key, val in self._registry.items():
            if val == cls:
                return key
        raise KeyError(cls)
