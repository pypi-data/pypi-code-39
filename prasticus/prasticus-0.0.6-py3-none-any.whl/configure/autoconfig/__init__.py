# configure/autoconfig/__init__.py
from .. import (path as configure_path, Action, Scanner, NotRecognized)
from ..lib.extend_module_path import ExtendModulePathAction
import warnings

def append_root_dir():
    from .manageroot import get_root_dir
    dir = get_root_dir()
    if dir:
        configure_path.append(str(dir))
    else:
        warnings.warn('Missing root directory for prasticus.configure. Create one with "python3 -W ignore -m prasticus.configure set-root --create DIR"')

append_root_dir()

class SelfScanner(Scanner):
    """class for autoconfiguration of configure module"""
    def __call__(self, item):
        if not isinstance(item, dict):
            raise NotRecognized(item)
        if item.get('purpose', None) == 'extend configuration path':
            return ExtendModulePathAction(
                item['idir'], relname='.loaded', item=item)
        raise NotRecognized(item)

scanner = SelfScanner
