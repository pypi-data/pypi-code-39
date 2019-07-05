# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 10:01:59 2018

@author: Carmen
"""

class InputError(BaseException):
    """
    Raised when Circuit class init argument is wrong
    """
    def __init__(self, message):
        super().__init__(message)