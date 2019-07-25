from .base import Action
from importlib import import_module
import re

_relname_pat = re.compile(r'^(?:[.][a-zA-Z_]\w*)?$')

class ExtendModulePathAction(Action):
    def __init__(self, idir, relname= '', item=None):
        """Action to extend __path__ of submodule with a sequence of directories
        
        Parameters:
            idir    : sequence of directories to add to the __path__
            relname : relative name of the target submodule (wr/ the configured module)
                      may be ''
            item    : the (optional) configuration item
        """
        super().__init__(item)
        self.relname = relname or ''
        if not _relname_pat.match(self.relname):
            raise ValueError('Invalid value for relname, got', relname)
        self.idir = list(idir)
        
    def __call__(self, module):
        submodule = import_module(module.__name__ + self.relname)
        submodule.__path__.extend(self.idir)