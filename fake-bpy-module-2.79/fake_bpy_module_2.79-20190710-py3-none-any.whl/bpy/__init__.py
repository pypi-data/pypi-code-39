import sys
import typing
from . import types
from . import utils
from . import ops
from . import props
from . import path
from . import app
from . import context

context: 'types.Context' = None

data: 'types.BlendData' = None
'''Access to Blenders internal data '''
