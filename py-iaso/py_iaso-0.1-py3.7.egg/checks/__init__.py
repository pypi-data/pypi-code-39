from importlib import import_module

from .default import DefaultCheck, NoopCheck
from .docker import DockerCheck
from .http import HttpCheck

from ..utils import raise_invalid_key, raise_missing_key, print_log

class Check:
    def __new__(cls, data_dict={}):
        if data_dict.get('enabled', True) == False:
            return NoopCheck()

        # if set(data_dict.keys()).isdisjoint(set(['type', 'data'])):
        #     raise_invalid_key('checks')
        _type = data_dict['type']

        if _type == 'docker':
            checker_class = DockerCheck
        elif _type == 'http':
            checker_class = HttpCheck
        else:
            module_name, class_name = _type.rsplit('.', 1)    
            try:
                checker_class = getattr(import_module(module_name), class_name)
            except (ModuleNotFoundError, AttributeError):
                raise_invalid_key('action: ' + data_dict['type'])

        data = data_dict.get('data')
        if type(data) == list:
            check = checker_class(*data)
        elif type(data) == dict:
            check = checker_class(**data)
        else:
            check = checker_class(data)
        
        return check