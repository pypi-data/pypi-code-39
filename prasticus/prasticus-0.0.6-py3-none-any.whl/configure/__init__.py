# configure/__init__.py

# The order of imports matters as some modules use imported symbols
from .loaded import __path__ as path 
from .lib.base import Action, NotRecognized, Scanner, all_of, some_of, first_of
from .engine import configure
from . import autoconfig
from .autoconfig.manageroot import configure_configure_name

# autoconfiguration du module configure
configure(
    __name__, configure_configure_name(), autoconfig.scanner)
del autoconfig

