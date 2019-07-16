# -*- coding: utf-8 -*-
#
from __future__ import print_function

from .__about__ import (
    __version__,
    __author__,
    __author_email__,
    __copyright__,
    __website__,
    __license__,
    __status__,
    __description__,
)

__doc__ = __description__

from .getdp_object import GetDPObject
from .problem_definition import Problem
from .group import Group
from .function import Function
from .constraint import Constraint
from .functionspace import FunctionSpace
from .jacobian import Jacobian
from .rendering import *


# from .helpers import generate_mesh, get_getdp_major_version, rotation_matrix

__all__ = ["__version__", "__author__", "__author_email__", "__website__"]

try:
    import pipdate
except ImportError:
    pass
else:
    if pipdate.needs_checking(__name__):
        print(pipdate.check(__name__, __version__), end="")
