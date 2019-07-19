#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Universal functions

    @author: tbbatbb
    @GitHub: https://github.com/tbbatbb
'''

import os, sys, traceback

reload(sys)
sys.setdefaultencoding('utf-8')

# Some macro definetion
HIDE_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'
F_BLACK  = '\033[;30m'
F_RED    = '\033[;31m'
F_GREEN  = '\033[;32m'
F_YELLOW = '\033[;33m'
F_BLUE   = '\033[;34m'
F_FUCHSIA= '\033[;35m'
F_CYAN   = '\033[;36m'
F_WHITE  = '\033[;37m'
C_DEFAULT= '\033[0m'
B_BLACK  = '\033[;40m'
B_RED    = '\033[;41m'
B_GREEN  = '\033[;42m'
B_YELLOW = '\033[;43m'
B_BLUE   = '\033[;44m'
B_FUCHSIA= '\033[;45m'
B_CYAN   = '\033[;46m'
B_WHITE  = '\033[;47m'

def err(e, tb=True):
    '''
        Print error information
    '''
    if tb:
        stack = traceback.extract_stack()
        caller_file = stack[-3][0]
        caller_func = stack[-3][2]
        line = stack[-3][1]
        print '[ {0}x{1} ] [{2}:{3}:{4}] {5}{6}'.format(F_RED, C_DEFAULT, os.path.basename(caller_file), caller_func, line, e, C_DEFAULT)
    else:
        print '[ {0}x{1} ] {2}'.format(F_RED, C_DEFAULT, e)


def info(i, tb=True):
    '''
        Print normal information
    '''
    if tb:
        stack = traceback.extract_stack()
        caller_file = stack[-3][0]
        caller_func = stack[-3][2]
        line = stack[-3][1]
        print '[ {0}√{1} ] [{2}:{3}:{4}] {5}{6}'.format(F_GREEN, C_DEFAULT, os.path.basename(caller_file), caller_func, line, i, C_DEFAULT)
    else:
        print '[ {0}√{1} ] {2}'.format(F_GREEN, C_DEFAULT, i)