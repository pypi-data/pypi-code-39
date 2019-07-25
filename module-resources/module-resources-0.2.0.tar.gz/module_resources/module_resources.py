import copy
import glob
import importlib.abc
import importlib.machinery
import importlib.util
import sys

from collections import namedtuple
from pathlib import Path

def _is_module_resource(candidate, name):
    return hasattr(candidate, '__module__') and candidate.__module__ == name


def _namedtuple_to_dict(value, name):
    if _is_module_resource(value, name):
        return dict(value)

    clean_value = None
    if isinstance(value, dict):
        clean_value = copy.deepcopy(value)
        for key, val in clean_value.items():
            if _is_module_resource(val, name):
                clean_value[key] = dict(val)
    return clean_value or value


class ImportableFallbackDict(dict):
    __spec__ = None


class ModuleResource:
    filename_glob = ''

    def __init__(self, module_name, module_path, filename_glob=None):
        self.name = module_name
        self.path = module_path
        if filename_glob:
            self.filename_glob = filename_glob

    def import_request_to_filepath(self, spec):
        filename = spec.name.replace(f'{self.name}.', '')
        return Path(self.path).parent / f'{filename}{Path(self.filename_glob).suffix}'

    def intercept_imports(self):
        loader = ModuleResourceLoader(self.create_module)
        finder = ModuleResourceFinder(self.name, loader, self.filename_glob)
        all_modules = [Path(filename).stem for filename in glob.glob(str(self.filename_glob))]
        sys.meta_path.append(finder)
        return all_modules

    def create_module(self, spec):
        raise NotImplementedError("Subclasses must define a create_module method")

    @staticmethod
    def mapping_to_namedtuple(mapping, spec, typename):
        def _iter_namedtuple_source(_):
            for key, value in mapping.items():
                yield key, _namedtuple_to_dict(value, spec.name)

        keys, values = mapping.keys(), mapping.values()
        try:
            mapping_namedtuple = namedtuple(typename, keys, module=spec.name)
        except ValueError:
            ImportableFallbackDict.__spec__ = spec
            ImportableFallbackDict.__iter__ = _iter_namedtuple_source
            ImportableFallbackDict.__all__ = list(keys)
            return ImportableFallbackDict(**mapping)

        mapping_namedtuple.__spec__ = spec
        mapping_namedtuple.__iter__ = _iter_namedtuple_source
        mapping_namedtuple.__all__ = list(keys)
        return mapping_namedtuple(*values)


class ModuleResourceFinder(importlib.abc.MetaPathFinder):
    def __init__(self, name, loader, glob_pattern):
        self.name = name
        self._loader = loader
        self.glob_pattern = glob_pattern

    def find_spec(self, fullname, *_, **__):
        if fullname.startswith(self.name):
            return importlib.util.spec_from_file_location(
                fullname,
                location=self.glob_pattern,
                loader=self._loader
            )
        return None


class ModuleResourceLoader(importlib.abc.Loader):
    def __init__(self, create_module):
        self.create_module = create_module

    def exec_module(self, _):
        pass

    def module_repr(self, _):
        pass
