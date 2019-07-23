
from ._change_block_classes import (
    ExecutedFunction,
    Loop,
    Variable,
    Function,
    IfStatement
)
ID_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def _base_len_ID_CHARS(num):
    numerals=ID_CHARS
    b=len(ID_CHARS)
    return ((num == 0) and numerals[0]) or (_base_len_ID_CHARS(num // b).lstrip(numerals[0]) + numerals[num % b])

def _new_ref_id(num):
    return _base_len_ID_CHARS(num)


class UnNestExecutedFunctions:

    def __init__(self):
        self.function_count = 0

    def _assign_references(self, last_change, executed_function):
        last_change.reference_id = _new_ref_id(self.function_count)
        executed_function.reference_id = _new_ref_id(self.function_count)
        self.function_count += 1
        return last_change, executed_function

    def _un_nest_changes(self, changes):
        found_functions = []
        new_changes = []
        for _, change in enumerate(changes):
            if type(change) is ExecutedFunction:
                new_changes[-1], change = self._assign_references(new_changes[-1], change)
                found_functions += self._executed_function(change)
            else:
                if type(change) is Loop:
                    change, new_functions = self._loop(change)
                    found_functions += new_functions
                new_changes.append(change)
        return new_changes, found_functions

    def _loop(self, loop):
        found_functions = []
        for i, changes in enumerate(loop.changes):
            new_changes, new_functions = self._un_nest_changes(changes)
            loop.changes[i] = new_changes
            found_functions += new_functions
        return loop, found_functions

    def _executed_function(self, executed_function):
        new_changes, found_functions = self._un_nest_changes(executed_function.changes)
        executed_function.changes = new_changes
        return [executed_function] + found_functions

    def run(self, executed_function):
        return self._executed_function(executed_function)

