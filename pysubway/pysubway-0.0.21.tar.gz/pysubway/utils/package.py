import inspect
import pkgutil
import sys
from importlib import import_module
from typing import Any
from typing import Dict


class Package(object):
    """
    find classes or variables from modules
    """

    def __init__(self, package_path: str):
        """
        :param package_path: such as 'apps.app.service'
        """
        self._classes = dict()
        self._attrs = dict()
        self.package_path = package_path

    def get_classes(self, prefix: str = '') -> Dict[str, Any]:
        """
        filter classes that has the prefix
        :param prefix:
        :return:
        """
        if not self._classes:
            import_module(self.package_path)
            module = sys.modules[self.package_path]
            module_path = module.__path__
            for i in pkgutil.iter_modules(module_path):
                import_module('.'.join((self.package_path, i.name)))
            for k, v in sys.modules.items():
                if k.startswith(self.package_path) and not k.startswith('_'):
                    for k, v in v.__dict__.items():
                        if inspect.isclass(v):
                            if prefix and k.startswith(prefix):
                                self._classes[k] = v
                            if not prefix:
                                self._classes[k] = v
        return self._classes

    def conf_attrs(self, upper: bool = False) -> Dict[str, Any]:
        if not self._attrs:
            import_module(self.package_path)
            module = sys.modules[self.package_path]
            for k, v in inspect.getmembers(module):
                if not inspect.isbuiltin(v):
                    if upper and k.isupper():
                        self._attrs[k] = v
                    if not upper:
                        self._attrs[k] = v
        return self._attrs
