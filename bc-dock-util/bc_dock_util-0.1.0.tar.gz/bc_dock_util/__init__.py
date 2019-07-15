# -*- coding:UTF-8 -*-

import sys

def is_python3():
    if (sys.version[0] == '3'):
        return True
    else:
        return False
        
        
if is_python3():
    from bc_dock_util.bc_dock_util import *
    import bc_dock_util.bc_dock_util as bc_dock_util
    __all__ = dir(bc_dock_util)
else:
    from bc_dock_util import *

name = 'bc_dock_util'

# 查了官方文档，下面的配置为非必须
# version_info = (0, 0, 9)