"""
-------------------------------------------------------------------------------

`thucyd.eigen` package import

-------------------------------------------------------------------------------
"""

# load .impl select functions into eigen namespace
from .impl import *  # noqa F403

# freeze API of the eigen subpackage
__all__ = impl.__all__  # noqa F405
