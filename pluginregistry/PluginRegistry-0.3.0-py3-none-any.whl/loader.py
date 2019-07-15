import importlib
import sys
from pkg_resources import iter_entry_points


class PluginLoader:
    def __init__(self, registry):
        # fmt: off
        self._registry = registry
        self._group    = registry._entry_point_group
        self._path     = registry.path
        self._cache    = None
        # fmt: on

    def enable(self):
        if self._group is not None and not self in sys.meta_path:
            sys.meta_path.append(self)

    def disable(self):
        try:
            sys.meta_path.remove(self)
        except ValueError:
            pass

    @property
    def plugins(self):
        if self._cache is None:
            self._cache = {}
            for ep in iter_entry_points(group=self._group):
                if ep.name.startswith(self._path):
                    self._cache[ep.name] = ep

        return self._cache

    def find_spec(self, fullname, path, target=None):
        # print(f"### find_spec(fullname={fullname}, path={path}, target={target})")
        if fullname in self.plugins:
            return importlib.machinery.ModuleSpec(
                fullname,
                self,
                origin=None,
                loader_state={
                    "group": self._group,
                    "entry_point": self.plugins[fullname],
                },
            )
        elif self._path.startswith(fullname) and self._registry.get(fullname):
            return importlib.machinery.ModuleSpec(
                fullname,
                self,
                origin=None,
                loader_state={
                    "group": self._group,
                    "entry_point": self._registry.get(fullname).entry_point,
                },
                is_package=self._registry.get(fullname).is_registry,
            )

    def create_module(self, spec):
        # print(f"### create_module({spec})")
        loaded = self._registry.get(spec.name)
        if loaded:
            obj = loaded
        elif spec.name in self.plugins:
            obj = spec.loader_state["entry_point"].load()
        else:
            raise ImportError(f"Module Not Found: {spec.name}")

        if obj.is_registry:
            # Transform the registry class into something that looks like a module.
            spec.submodule_search_locations = [obj.path]

            # fmt: off
            obj.__name__    = obj.path
            obj.__path__    = [obj.path]
            obj.__spec__    = spec
            obj.__package__ = spec.name
            obj.__loader__  = self
            # fmt: on

        return obj

    def exec_module(self, module):
        pass
