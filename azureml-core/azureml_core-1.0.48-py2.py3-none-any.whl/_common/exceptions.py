# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import sys
import traceback


class AzureMLException(Exception):
    """
    Base class for all azureml exceptions.
    Extends Exception, if trying to catch only azureml exceptions
    then catch this class.
    """

    def __init__(self, exception_message, inner_exception=None, **kwargs):
        Exception.__init__(self, exception_message, **kwargs)
        self._exception_message = exception_message
        self._inner_exception = inner_exception
        self._exc_info = sys.exc_info()

    @property
    def message(self):
        return self._exception_message

    @message.setter
    def message(self, value):
        self._exception_message = value

    @property
    def inner_exception(self):
        return self._inner_exception

    @inner_exception.setter
    def inner_exception(self, value):
        self._inner_exception = value

    def print_stacktrace(self):
        traceback.print_exception(*self._exc_info)
