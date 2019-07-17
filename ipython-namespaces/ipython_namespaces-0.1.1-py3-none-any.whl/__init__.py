from .namespaces import Namespaces

__version__ = '0.1.0'


def load_ipython_extension(ipython):
    ipython.register_magics(Namespaces)
