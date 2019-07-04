from typing import Any, Dict, Optional

from ._packable import Packable
from ._packer import Packer
from ._resolver import Resolver

__version__ = "0.1.0"
__all__ = ("pack", "unpack", "packable",)


_resolver = Resolver()
_packer = Packer(_resolver)
packable = Packable(_resolver)


def pack(packable: Any) -> bytes:
    return _packer.pack(packable)


def unpack(packed: bytes, ext_resolvers: Optional[Dict[Any, Any]] = None) -> Any:
    return _packer.unpack(packed, ext_resolvers)
