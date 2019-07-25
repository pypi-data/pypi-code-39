# module prasticus.configure.engine
from . import loaded
from .lib.base import Scanner, NotRecognized
from functools import partial
from importlib import import_module
import sys

class Agent:
    def __init__(self, module, key, callback, scanner):
        self.module = module
        self.static_module = None
        self.key = key
        self.callback = callback
        self.scanner = scanner

    def update(self, iitem):
        for g in iitem:
            self.callback(g, self.module)
            
def _quiet_wrapper(callback, *args, **kwargs):
    try:
        return callback(*args, **kwargs)
    except NotRecognized:
        return None
    

def configure(name_or_module, key, method, quiet=False):
    scanner = None
    if isinstance(method, type) and issubclass(method, Scanner):
        scanner = method()
        callback = scanner.callback
        if quiet:
            callback = partial(_quiet_wrapper, callback)
    elif isinstance(method, Scanner):
        scanner = method
        callback = scanner.callback
        if quiet:
            callback = partial(_quiet_wrapper, callback)
    elif callable(method):
        callback = method
    else:
        raise ValueError(
            'Expected callable third argument to configure(), got', method)
    module = import_module(name_or_module) if isinstance(name_or_module, str) else name_or_module 
    agent = Agent(module, key, callback, scanner)
    try:
        config_mod = import_module('.' + key, loaded.__name__)
    except ImportError:
        pass
    else:
        agent.static_module = config_mod
        agent.update(config_mod.iconfigure(agent.module))
        agent.module._configure_agent = agent
    return agent
