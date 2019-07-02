#!/usr/bin/env python
import os
import public

"""
from django_find_apps import find_apps

INSTALLED_APPS = find_apps(".") + [
    ...
]
"""

def ispackage(path):
    return os.path.exists(os.path.join(path, '__init__.py'))

def isapp(path):
    return os.path.basename(path) not in ["migrations","templatetags"]

def find_package_dirs(path):
    for root, dirs, files in os.walk(path):
        _dirs = dirs[:]
        dirs = []
        for _dir in _dirs:
            fullpath = os.path.join(root, _dir)
            if ispackage(fullpath):
                yield fullpath
                dirs.append(_dir)

@public.add
def find_apps(path):
    """return a list of apps"""
    apps = []
    for _dir in filter(isapp,find_package_dirs(path)):
        relpath = os.path.relpath(_dir, path)
        apps.append(relpath.replace(os.path.sep, '.'))
    return apps
