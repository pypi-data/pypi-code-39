#!/usr/bin/env python
# -*-coding: utf8-*-
'''__init__ # (prasticus.catchall)

Pour traverser tous les plugins disponibles, utiliser

    for loader, name, ispkg in pkgutil.iter_modules(__path__)
'''

from prasticus import configure
from prasticus.configure.lib.extend_module_path import ExtendModulePathAction

class _Scanner(configure.Scanner):
    def __call__(self, item):
        if item.get('purpose', '') == 'extend module path':
            return ExtendModulePathAction(item['idir'], item=item)
        else:
            raise configure.NotRecognized(item)

configure.configure(
    __name__, "laf2pu2uenx83qhwigwkiqioa", _Scanner)
