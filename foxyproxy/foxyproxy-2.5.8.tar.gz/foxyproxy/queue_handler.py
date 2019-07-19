#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module:
***

https://mattgathu.github.io/multiprocessing-logging-in-python/

 Copyright (C) Smart Arcs Ltd, registered in the United Kingdom.
 This file is owned exclusively by Smart Arcs LTd.
 Unauthorized copying of this file, via any medium is strictly prohibited
 Proprietary and confidential
 Written by Dan Cvrcek <support@smartarchitects.co.uk>, Feb 2019
"""
__author__ = "Dan Cvrcek"
__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@smartarchitects.co.uk'
__status__ = 'Development'

import sys
import logging
import traceback
import threading
import multiprocessing
# noinspection PyPep8Naming
from logging import FileHandler as FH


# ============================================================================
# Define Log Handler
# ============================================================================
# noinspection PyMissingOrEmptyDocstring
class QueueHandler(logging.Handler):
    """multiprocessing log handler

    This handler makes it possible for several processes
    to log to the same file by using a queue.

    """
    def __init__(self, fname=None):
        logging.Handler.__init__(self)

        if fname:
            self._handler = FH(fname)
        else:
            self._handler = logging.StreamHandler(sys.stderr)

        self.queue = multiprocessing.Queue(-1)

        thrd = threading.Thread(target=self.receive, name="log listener")
        thrd.daemon = False
        thrd.start()

    def setFormatter(self, fmt):
        logging.Handler.setFormatter(self, fmt)
        self._handler.setFormatter(fmt)

    def setLevel(self, level):
        self._handler.setLevel(level)

    def receive(self):
        while True:
            try:
                record = self.queue.get()
                self._handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except BaseException:
                traceback.print_exc(file=sys.stderr)

    def send(self, s):
        self.queue.put_nowait(s)

    def _format_record(self, record):
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            # noinspection PyUnusedLocal
            dummy = self.format(record)
            record.exc_info = None

        return record

    def emit(self, record):
        # noinspection PyBroadException
        try:
            s = self._format_record(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        self._handler.close()
        logging.Handler.close(self)