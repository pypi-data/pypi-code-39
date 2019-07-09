# -*- coding: utf-8 -*-
 
 
"""odut.__main__: execute odut directory is called as script.

Certain workflows require the odut directory to be treated as both a package 
and as the main script, via $ python -m odut invocation. 
Actually, this calls the __main__.py file if existing (or fails if not).
"""

# from .cli import main
# main()