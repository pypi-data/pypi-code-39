"""
Short for Seeq PYthon, the Spy library provides methods to interact with data that is exposed to the Seeq Server.
"""

from . import assets

from ._login import login
from ._plot import plot
from ._pull import pull
from ._push import push
from ._search import search

__all__ = ['assets', 'login', 'plot', 'pull', 'push', 'search']
