from typing import Any, Union, cast

from ._resolver import AnyClass, Resolver

__all__ = ("Packable",)


class Packable:
    def __init__(self, resolver: Resolver) -> None:
        self._resolver = resolver

    def __call__(self, cls_or_name: Union[str, AnyClass]) -> Any:
        if not isinstance(cls_or_name, str):
            self._resolver.register(cls=cls_or_name)
            return cls_or_name

        def wrapped(cls: AnyClass) -> AnyClass:
            self._resolver.register(cls=cls, name=cast(str, cls_or_name))
            return cls

        return wrapped
