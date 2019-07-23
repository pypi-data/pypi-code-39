import sys
from importlib import import_module
import yaml
import pathlib
from typing import Callable
from ..exceptions import FileTypeNotSupported
import os
from logging import getLogger
import json
import pkgutil

logger = getLogger(__name__)


def reraise_import_module_exception(module_name, e):
    missing_module_re = f"^No module named '?{module_name}'?$"
    if re.match(missing_module_re, str(e)):
        raise Exception(f'Module {module_name} not found')
    raise e


def try_to_import_module_by_name(module_name):
    parts = module_name.split(":", 1)
    success = True
    module = None
    if len(parts) == 1:
        module_name, obj = module_name, None
    else:
        module_name, obj = parts[0], parts[1]
    try:
        import_module(module_name)
        module = sys.modules[module_name]
    except ImportError as e:
        # reraise_import_module_exception(module_name, e)
        logger.exception(f'Error importing module `{module_name}`: {e}')
        success = False
    return success, module_name, module, obj


def decorator_containers_from_module(module_name, container_extractor: Callable, **kwargs):
    _is_submodule: bool = kwargs['_is_submodule'] if kwargs and '_is_submodule' in kwargs else False
    containers = list()
    module_loaded, module_name, module, obj = try_to_import_module_by_name(module_name)
    if module_loaded:
        if obj is None:
            containers.extend(container_extractor(module))
            if not len(containers) and not _is_submodule:
                logger.info(f'Decorator containers not found in module `{module_name}`. '
                            'Trying to search in submodules...')
                for importer, modname, ispkg in pkgutil.iter_modules(module.__path__):
                    if not ispkg:
                        logger.info(f'Inspecting submodule `{module_name}.{modname}`')
                        containers_sub = decorator_containers_from_module(f'{module_name}.{modname}',
                                                                          container_extractor,
                                                                          _is_submodule=True)
                        logger.info(f'Found {len(containers_sub)} decorator container(s) '
                                    f'in submodule `{module_name}.{modname}`.')
                        containers.extend(containers_sub)
                    else:
                        logger.debug(f'Submodule `{module_name}.{modname}` skipped, it is package')
        else:
            try:
                container = getattr(module, obj)
                if not isinstance(container, type):
                    logger.error('Decorator container must be a class. '
                                 f'Instead, object `{module_name}:{obj}` '
                                 f'of type {type(container).__name__} was found.')
                else:
                    containers.append(container)
            except AttributeError:
                logger.exception(f'Failed to find decorator container {obj} in module {module_name}.')
    return containers


def load_config(path: str = 'config.yml'):
    ext = (pathlib.Path(path).suffixes[-1]).lower()
    if ext == '.yml' or ext == '.yaml':
        return load_yaml_file(path)
    elif ext == '.json':
        return load_json_file(path)
    raise FileTypeNotSupported(f'Config file of type `{ext}` is not supported.')


def load_yaml_file(path):
    if os.path.exists(path):
        with open(path, 'rt') as f:
            return yaml.full_load(f)
    raise FileNotFoundError(f'Config file of type `{path}` not found.')


def load_json_file(path):
    if os.path.exists(path):
        with open(path, 'rt') as f:
            return json.load(f)
    raise FileNotFoundError(f'Config file of type `{path}` not found.')


def load_config_section(path: str, config_section: str):
    extra_config = load_config(path)
    if config_section in extra_config:
        return extra_config[config_section]
    return None
