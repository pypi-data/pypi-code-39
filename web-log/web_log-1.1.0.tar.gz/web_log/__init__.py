"""web_log is a lightweight thin logger that logs against a logger service.

Currently it logs against st-vsib:4444, but this is runtime configurable
by setting

* web_log.constants.WEBLOG_SERVER
* web_log.constants.WEBLOG_PORT
* web_log.constants.WEBLOG_PATH

to whichever logger you want to use.

Usage:

>>> from web_log import log
>>> log('My app', 'launch')


>>> from web_log import log
>>> log('My app', 'launch', user='Jenkins', extra_info='caught exception', async_=True)

Can also be used in scripts or from terminal with
/project/res/bin/wlog MyApp MyEvent Some extra information goes here

"""

from .web_log_functions import LogSync, LogAsync, log, WEBLOG_VERSION
from .constants import *
from .statoil_log_handler import StatoilLogHandler
from .wlog import wlog

__version__ = WEBLOG_VERSION
__author__ = "Software Innovation, Equinor ASA"

__all__ = ["LogSync", "LogAsync", "log", "StatoilLogHandler"]
