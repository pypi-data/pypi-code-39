import os
import utail_base
import logging
import html
import re
from .string_support import clean_html
import threading
from timeit import default_timer as timer
from .web_support import HttpError
from .selenium_pool import SeleniumPool

def processBootStrap(useChdir=True, useLogger=True, logFilePath='/tmp/logFileName.log', filePath=''):
    if useChdir is True:
        dir_path = os.path.dirname(os.path.realpath(filePath))
        parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))
        os.chdir(parent_path)

    if useLogger is True:
        # setup logging
        utail_base.setup_logging(default_level=logging.INFO)
        utail_base.setup_logging_root(loggingLv=logging.DEBUG, filePath=logFilePath)
