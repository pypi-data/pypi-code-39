import os
from importlib import import_module

def _copy_attrs_from_module(namespace, modname):
    try:
        mod = import_module(modname)
        for key, value in mod.__dict__.items():
            if not key.startswith('__'):
                namespace[key] = value

        print('yaset imported local settings: %s' % modname)
    except ModuleNotFoundError:
        print('yaset could not load local settings: %s' % modname)


def import_settings(namespace):
    redirect = os.path.join(os.path.dirname(namespace['__file__']), 
        'local_settings/import_redirect')

    try:
        with open(redirect, 'r') as f:
            module_name = f.read().strip()
    except FileNotFoundError:
        print(('Error! yaset could not load "import_redirect" file, '
            'cannot import custom settings'))
        return

    _copy_attrs_from_module(namespace, 
        '%s.local_settings.%s' % (namespace['__package__'], module_name))

    _copy_attrs_from_module(namespace, '%s.local_settings.secrets.%s' % (
        namespace['__package__'], module_name))
