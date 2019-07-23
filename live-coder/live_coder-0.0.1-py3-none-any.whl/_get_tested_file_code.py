'''
Gets code from a tested script.
'''
import ast

from ._testing_code_file import TestingCodeFile
from ._constants import (
    TEST_PROJECT_FOLDER
)

TESTED_FILE_PATH = './demo_project/src/main.py'
TEST_LINE_NO_BOUNDS = [2, 9]


def _function_body_start(commands, name):
    for i, command in enumerate(commands):
        if type(command) is ast.FunctionDef and command.name == name:
            return i
    raise RuntimeError('Could not find definition for function with name:' + name)

def _last_tab_i(lines):
    return None

def _function_end(lines, commands, command_i):
    if command_i+1 >= len(commands):
        return len(lines) - 1
    return commands[command_i+1].lineno -1

def _function_bounds(lines, name):
    root = ast.parse('\n'.join(lines))
    commands = root.body
    command_i = _function_body_start(commands, name)
    def_start = commands[command_i].lineno
    body_start = commands[command_i].body[0].lineno - 1
    end = _function_end(lines, commands, command_i)
    return def_start, body_start, end


def testingCodeFile_from_method(method):
    '''
        Makes a testing code file for a given method.

        params:
            method in the form {folder}.{filename}.{function}
        returns:
            TestingCodeFile for the function.
    '''
    folder, filename, function = method.split('.')
    path = TEST_PROJECT_FOLDER + '/' + folder + '/' + filename + '.py'
    lines = open(path, 'r').read().split('\n')
    def_start, body_start, end = _function_bounds(lines, function)
    return TestingCodeFile(path, lines, def_start, body_start, end)
