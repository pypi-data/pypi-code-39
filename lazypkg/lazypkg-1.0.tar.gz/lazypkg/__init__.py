# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 20:26:38 2019

@author: yoelr
"""
import sys
from importlib import import_module
from types import ModuleType

__all__ = ('LazyPkg',)

class LazyPkg(ModuleType):
    """Cast module as a LazyPkg object that allows for lazy import of subpackages and direct access to subpackage objects.
    
    **Parameters**
    
        **__name__:** [str] Name of module.
        
        **subpackages:** iterable[str] Names of subpackages to be lazy imported.
        
        **delete:** iterable[str] Objects to be deleted from package.
    
    """
    def __new__(cls, __name__, subpackages, delete=('LazyPkg',)):
        self = sys.modules[__name__]
        if hasattr(self, '__all__'):
            __all__ = self.__all__
            for i in subpackages:
                if i in __all__:
                    raise ValueError(f"module '{i}' already in {__name__}.__all__")
            try:
                __all__.extend(subpackages)    
            except AttributeError:
                RuntimeError("'{__name__}.__all__'  must be a list")
        else:
            self.__all__ = list(subpackages)
        self.__class__ = LazyPkg
        for i in delete: delattr(self, i)
    
    def __dir__(self):
        return self.__all__ + list(self.__dict__)
    
    def __getattr__(self, name):
        try: attr = import_module('.'+name, self.__package__)
        except ImportError:
            for i in self.__all__:
                module = getattr(self, i)
                if isinstance(module, ModuleType) and hasattr(module, name):
                    attr = getattr(module, name)
                    break
        try: setattr(self, name, attr)
        except NameError:
            raise AttributeError(f"module {self.__name__} has no attribute '{name}'")
        return attr
    