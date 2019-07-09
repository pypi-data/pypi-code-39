# -*- coding: utf-8 -*-
"""

@author: Donggeun Kwon (donggeun.kwon@gmail.com)

Cryptographic Algorithm Lab.
Graduate School of Information Security, Korea University

"""

# from .custom_setup import __setup__
# __setup__()

__version__ = '0.0.4'
__doc__ = 'https://notify-bot.line.me/doc/en/'
__name__ = 'LineNoti'

__all__ = ['__version__', 
		   '__doc__', 
		   '__name__',
		   'notifier']

from .main import Notifier as notifier