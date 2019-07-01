"""Flat tree module."""

from flat_tree.accessor import FlatTreeAccessor  # noqa
from flat_tree.iterator import FlatTreeIterator  # noqa

try:
    import pkg_resources
except ImportError:
    pass


try:
    __version__ = pkg_resources.get_distribution('flat_tree').version
except Exception:
    __version__ = 'unknown'
