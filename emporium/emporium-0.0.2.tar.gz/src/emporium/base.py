import io
import os
from abc import ABC, abstractmethod
from contextlib import contextmanager
from enum import Enum

from emporium.utils import select_keys


class Encoding(Enum):
    BINARY = "b"
    STRING = ""


class AbstractStore(ABC):
    """
    Interface for data stores.  Allows reading and writing file-like object by
    path.
    """

    @abstractmethod
    @contextmanager
    def read(self, path, encoding):
        """Context manager that provides a read-only stream.

        :param path: The (relative) location of the file backing the stream.

        :returns: A read-only stream (a file-like object).
        """
        pass

    @abstractmethod
    @contextmanager
    def write(self, path, encoding):
        """Context manager that provides a writable stream.

        :param path: The (relative) location of the file backing the stream.

        :returns: A writeable stream (file-like object).
        """
        pass


class LocalStore(AbstractStore):
    """Store that puts data on the local disk."""

    def __init__(self, base_path=None):
        """Instantiate a store.

        :param base_path: The root path of the store.

        :returns: Instance that implements :class:`~emporium.base.AbstractStore`.
        """
        self._base_path = base_path

    @classmethod
    def from_config(cls, config):
        return cls(**select_keys(config, "base_path"))

    @contextmanager
    def read(self, path, encoding=Encoding.STRING):
        mode = "rb" if encoding == Encoding.BINARY else "r"
        with open(self._expand_path(path), mode) as handle:
            yield handle

    @contextmanager
    def write(self, path, encoding=Encoding.STRING):
        full_path = self._expand_path(path)
        self._ensure_dir_exists(full_path)
        mode = "wb" if encoding == Encoding.BINARY else "w"
        with open(self._expand_path(path), mode) as handle:
            yield handle

    def _expand_path(self, path):
        if self._base_path is None:
            return path
        return os.path.join(self._base_path, path)

    @staticmethod
    def _ensure_dir_exists(full_path):
        try:
            os.makedirs(os.path.dirname(full_path))
        except OSError:
            pass

    def __repr__(self):
        return "<{}({})>".format(self.__class__.__name__, self._base_path)


class InMemoryStore(AbstractStore):
    """Store that keeps data in memory."""

    def __init__(self):
        """Instantiate a store.

        :returns: Instance that implements :class:`~emporium.base.AbstractStore`.
        """
        self._data = {}

    @classmethod
    def from_config(cls, config):
        # pylint: disable=unused-argument
        return cls()

    @contextmanager
    def write(self, path, encoding=Encoding.STRING):
        resource = io.StringIO()
        yield resource
        resource.seek(0)
        self._data[path] = resource.read()

    @contextmanager
    def read(self, path, encoding=Encoding.STRING):
        yield io.StringIO(self._data[path])

    def read_raw(self, path):
        return self._data.get(path)

    def write_raw(self, path, contents):
        self._data[path] = contents

    def __repr__(self):
        return "<{}()>".format(self.__class__.__name__)


class ChimearicIO(io.BytesIO):
    """BytesIO wrapper that additionally takes care of encoding strings before
    writing them to the bytes buffer.
    """

    def write(self, s):
        if isinstance(s, str):
            super().write(s.encode("utf8"))
        else:
            super().write(s)
