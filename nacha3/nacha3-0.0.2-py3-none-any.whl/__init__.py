from __future__ import absolute_import

import sys

if sys.version_info[0] < 3:
    from .nacha2_init import *
else:
    from .nacha3_init import *

