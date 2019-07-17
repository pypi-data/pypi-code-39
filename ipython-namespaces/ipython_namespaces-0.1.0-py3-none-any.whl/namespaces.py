from IPython.core.magic import Magics, magics_class, cell_magic


class FallbackDict(dict):
    """
    Dict subclass that takes values from a fallback dict if they are not in self
    """

    def __init__(self, fallback):
        self.fallback = fallback

    def __missing__(self, key):
        return self.fallback[key]

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exception:
            raise AttributeError from exception


class ItemAttr(type(Magics)):
    """Metaclass that allows attribute access to namespaces"""

    def __getattr__(cls, name):
        try:
            return cls.namespaces[name]
        except KeyError as exception:
            raise AttributeError from exception


@magics_class
class Namespaces(Magics, metaclass=ItemAttr):
    """Encapsulation of the state of all namespaces"""

    namespaces = {}

    @cell_magic
    def space(self, line, cell):
        name = line.strip()
        namespace = self.namespaces.setdefault(name, FallbackDict(self.shell.user_ns))
        user_ns_backup, self.shell.user_ns = self.shell.user_ns, namespace
        self.shell.run_cell(cell)
        self.shell.user_ns = user_ns_backup
