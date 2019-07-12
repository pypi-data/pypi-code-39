import functools
from importlib import import_module

from ..utils import raise_invalid_key, raise_missing_key, print_log

class Action:
    def __new__(self, data_dict):
        if data_dict.get('enabled', True) == False:
            return lambda: None

        _type = data_dict['type']
        if '.' not in _type:
            module_name = 'pyiaso.actions.helpers'
            func_name = _type
        else:
            module_name, func_name = data_dict['type'].rsplit('.', 1)
        
        try:
            func = getattr(import_module(module_name), func_name)
        except (ModuleNotFoundError, AttributeError):
            raise_invalid_key('action: ' + _type)

        data = data_dict.get('data', None)

        if type(data) == list:
            return functools.partial(func, *data)
        elif type(data) == dict:
            return functools.partial(func, **data)
        else:
            return func