from typing import Any, Dict, Optional

from umsgpack import Ext, dumps, loads

from ._resolver import Resolver

__all__ = ("Packer",)


class Packer:
    def __init__(self, resolver: Resolver) -> None:
        self._resolver = resolver

    def _pack(self, packable: Any) -> Ext:
        cls_name = self._resolver.resolve_name(type(packable))
        return Ext(0x42, self.pack([cls_name, packable.__packed__()]))

    def pack(self, packable: Any) -> bytes:
        return dumps(packable, ext_handlers={object: self._pack})  # type: ignore

    def _unpack(self, packed: bytes, ext_resolvers: Dict[Any, Any]) -> Any:
        cls_name, kwargs = self.unpack(packed, ext_resolvers)
        resolved = self._resolver.resolve_type(cls_name)

        for cls, resolver in ext_resolvers.items():
            if issubclass(resolved, cls):
                return resolver(resolved, **kwargs)

        if hasattr(resolved, "__unpacked__"):
            return resolved.__unpacked__(**kwargs)
        return resolved(**kwargs)

    def unpack(self, packed: bytes, ext_resolvers: Optional[Dict[Any, Any]] = None) -> Any:
        return loads(packed, ext_handlers={
            0x42: lambda x: self._unpack(x.data, ext_resolvers or {}),
        })
