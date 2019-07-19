# import io
from contextlib import contextmanager

from emporium.base import AbstractStore


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
    def open(self, path, mode, *args, **kwargs):
        raise NotImplementedError()

    def substore(self, path):
        raise NotImplementedError()

    # @contextmanager
    # def write(self, path, encoding=Encoding.STRING):
    #     resource = io.StringIO()
    #     yield resource
    #     resource.seek(0)
    #     self._data[path] = resource.read()

    # @contextmanager
    # def read(self, path, encoding=Encoding.STRING):
    #     yield io.StringIO(self._data[path])

    def read_raw(self, path):
        return self._data.get(path)

    def write_raw(self, path, contents):
        self._data[path] = contents

    def __repr__(self):
        return "<{}()>".format(self.__class__.__name__)
