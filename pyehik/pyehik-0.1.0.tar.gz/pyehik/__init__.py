# -*- coding: utf-8 -*-

"""Top-level package for pyehik."""

__author__ = """Jovany Leandro G.C"""
__email__ = 'bit4bit@riseup.net'
__version__ = '0.1.0'
import ctypes
from . import config

def load_sdk(pathname):
    HC = ctypes.cdll.LoadLibrary(pathname)

    from . import sdk
    sdk.HC = HC
    return sdk

