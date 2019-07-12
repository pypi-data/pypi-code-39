from abc import ABCMeta, abstractmethod
from functools import wraps
from ..utils import print_log

def pre_init(self):
    self.failure = None
    self.recovery = None
    self.name = self.__class__.__name__
    
class DefaultCheckMeta(type):
    def __new__(metacls, name, bases, attributedict, **kwargs):
        if 'check' in attributedict and callable(attributedict['check']):
            f = attributedict['check']
            @wraps(f)
            def my_func(self, *args, **kwargs):
                if self.failure:
                    self.recovery = self.failure
                return f(self, *args, **kwargs)

            attributedict['check'] = my_func
        
        instance = super().__new__(metacls, name, bases, attributedict, **kwargs)
        # if name is not 'DefaultCheck':
        #     pre_init(instance)
        return instance
    
    def __init__(self, cls_name, superclasses, attributedict, **kwargs):
        if cls_name is not 'DefaultCheck':
            self.failure = None
            self.recovery = None
        self.name = cls_name

        
class DefaultCheck(metaclass=DefaultCheckMeta):
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
