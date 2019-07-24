import inspect
import os
import pkgutil
from importlib import import_module

from django.apps import apps

from .provider import DataProvider
from .registry import register_provider


def find_datahook_commands():
    for app in apps.get_app_configs():
        path = os.path.join(app.path, 'datahooks')
        for module in pkgutil.iter_modules([path]):
            module = import_module('%s.datahooks.%s' % (app.name, module.name))
            for name in dir(module):
                obj = getattr(module, name)
                if not inspect.isclass(obj):
                    continue
                if obj is not DataProvider and issubclass(obj, DataProvider):
                    register_provider(obj)
