from abc import ABCMeta, abstractmethod
from functools import wraps
from ..utils import print_log

# Metaclass
class DefaultCheckMeta(type):
    def __new__(metacls, name, bases, attributedict, **kwargs):
        # Hack the check() method to add failure / recovery info
        if 'check' in attributedict and callable(attributedict['check']):
            f = attributedict['check']
            @wraps(f)
            def my_func(self, *args, **kwargs):
                if self.failure:
                    self.recovery = self.failure
                return f(self, *args, **kwargs)

            attributedict['check'] = my_func
        
        instance = super().__new__(metacls, name, bases, attributedict, **kwargs)
        return instance
    
    def __init__(self, cls_name, superclasses, attributedict, **kwargs):
        if cls_name is not 'DefaultCheck':
            self.failure = None
            self.recovery = None
        self.name = cls_name

        
class DefaultCheck(metaclass=DefaultCheckMeta):
    # We want to call classes directly for simpler syntax
    # Calling a SomethingCheck class will run its check() method
    def __call__(self, *args, verbose=False, **kwargs):
        if verbose:
            print_log('Checking again:', self.__class__.__name__)
        
        status = self.check(*args, **kwargs)
        
        if not status and self.failure:
            print_log(self.__class__.__name__, self.failure)
        return status

    @abstractmethod
    def check(self):
        raise NotImplementedError('Check not implemented')

class NoopCheck(DefaultCheck):
    def check(self):
        return True
