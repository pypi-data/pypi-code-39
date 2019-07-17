import logging
import pkg_resources

from .classproperty import classproperty
from .loader import PluginLoader

_logger = logging.getLogger(__name__)


class RegistryMeta(type):
    def __prepare__(metacls, *arg, **kw):
        return {"_plugins": {}}

    def __new__(metacls, clsname, bases, dct, **kw):
        # fmt: off
        dct["__getattr__"]  = classmethod(metacls.__getattr__)
        dct["__getitem__"]  = classmethod(metacls.__getitem__)
        dct["__contains__"] = classmethod(metacls.__contains__)
        dct["__dir__"]      = classmethod(metacls.__dir__)
        dct["__str__"]      = classmethod(metacls.__str__)
        dct["get"]          = classmethod(metacls.get)
        # fmt: on

        return super().__new__(metacls, clsname, bases, dct, **kw)

    def __getattr__(cls, key):
        children = {_._name: _ for _ in cls._children}
        if key in children:
            return children[key]
        elif key in cls._plugins:
            return cls._plugins[key]
        else:
            raise AttributeError(
                f"Registry '{cls.path}' does not contain a registry/plugin '{key}'"
            )

    def __getitem__(cls, key):
        children = {_._name: _ for _ in cls._children}
        if key in children:
            return children[key]
        elif key in cls._plugins:
            return cls._plugins[key]
        else:
            raise KeyError(f"Key '{key}' not found in class '{cls._name}'")

    def __dir__(cls):
        return (
            set(super().__dir__())
            | set(_._name for _ in cls._children)
            | cls._plugins.keys()
        )

    def __contains__(cls, item):
        return item in cls._plugins or item in {_._name for _ in cls._children}

    def get(cls, path, default=None):
        if type(path) != str:
            path = ".".join(path)

        if path == cls.path:
            return cls
        else:
            parts = path.replace(f"{cls.path}.", "").split(".")

            if not parts[0] in cls:
                return default
            elif len(parts) == 1:
                return cls[parts[0]]
            else:
                return cls[parts[0]].get(parts[1:])

    def __str__(cls):  # pragma: no cover
        return f"<Plugin Registry '{cls.path}'>"


class Registry(metaclass=RegistryMeta):
    _entry_point_group = "Registry"

    # fmt: off
    _base     = True
    _children = []
    _loader   = None
    _name     = __name__
    _parent   = None
    # fmt: on

    def __init_subclass__(cls, parent=None, *, base=False):
        # fmt: off
        cls._base     = base
        cls._children = []            # Redefined so that each class has a unique container
        cls._name     = cls.__name__  # Saved so that __name__ can be used by import loader
        cls._parent   = parent
        # fmt: on

        # Registry this class with its parent
        # ... this makes the chain registry chain bi-directional
        if cls._parent is not None:
            cls._parent._children.append(cls)

    @classproperty
    def is_registry(self):
        return True

    @classproperty
    def is_plugin(self):
        return False

    @classmethod
    def load_entry_point(cls, item):  # pragma: no cover
        """
        Attempt to load a module based on a plugin registry value
        """
        key = f"{cls.path}.{item}"
        module = None
        for entry_point in pkg_resources.iter_entry_points(
            group=cls._entry_point_group, name=key
        ):
            module = entry_point.load()

        if item in cls:
            return cls[item]
        else:
            raise AttributeError(
                f"Attempt to auto-load '{item}' via entry-point failed"
            )

    @classproperty
    def registries(cls):
        return tuple(cls._children)

    @classproperty
    def registry(cls):
        if cls.parent is object or cls._base:
            return None
        else:
            return cls.parent

    @classproperty
    def plugins(cls):
        return tuple(cls._plugins.values())

    @classproperty
    def path(cls):
        if cls._base or cls._parent is object:
            return cls._name
        else:
            return f"{cls._parent.path}.{cls._name}"

    @classproperty
    def plugin_tree(cls):  # pragma: no cover
        return sorted(
            [_.path for _ in cls._plugins.values()]
            + [path for child in cls._children for path in child.plugin_tree]
        )

    @classproperty
    def registry_tree(cls):  # pragma: no cover
        return sorted(
            [cls.path]
            + [path for child in cls._children for path in child.registry_tree]
        )

    @classproperty
    def tree(cls):  # pragma: no cover
        return sorted(cls.registry_tree + cls.plugin_tree)

    @classproperty
    def parent(cls):
        return cls._parent

    @classproperty
    def entry_point(cls):
        """
        Obtain an entry point object suitable for obtaining the string which needs to be
        used in setup.py for automatic plugin detection.  Not suitable for loading the
        module because the distribution has not been set.  However, to use this
        property, the module must already be loaded....
        """
        # Obtaining the real distribution is a VERY slow process
        # ... (more than 60% of unit test execution time)
        # ... for real module loading, obtaining the distribution would be necessary
        # ... but this object is used strictly for printing out entry point values
        #     for setup.py.
        # Thus, do not look up the distribution to save execution time.
        # ... This is reasonable because in order to use this method, the entry
        #     point must already be loaded!
        return pkg_resources.EntryPoint(
            cls.path, cls.__module__, (cls._name,), dist=None
        )

    @classmethod
    def entry_points(cls, module=None, *, align=True):
        entry_points = [
            cls.get(_).entry_point
            for _ in cls.tree
            if cls.get(_).entry_point is not None
        ]

        if not align and module is None:
            return sorted([str(_) for _ in entry_points])

        else:
            ep_parts = [str(_).split(" = ") for _ in entry_points]
            filtered = list(
                filter(lambda _: module is None or _[1].startswith(module), ep_parts)
            )
            length = max(len(_[0]) for _ in filtered)
            return sorted([f"{_[0]:{length}s} = {_[1]}" for _ in filtered])

    @classmethod
    def print_entry_points(
        cls, module=None, *, align=True, variable="entry_points"
    ):  # pragma: no cover
        eps = cls.entry_points(module, align=align)
        indented = "\n".join(f"""{' ':4}"{_}",""" for _ in eps)
        print(f"""{variable} = [\n{indented}\n]""")

    @classmethod
    def load_entry_points(cls, group=None, exclude=[]):  # pragma: no cover
        if group is None:
            group = cls._entry_point_group

        for ep in pkg_resources.iter_entry_points(group=group):
            if cls.get(ep.name) is None:
                try:
                    module = ep.load()
                except ImportError as ex:
                    _logger.warning(f"Failed to import plugin {ep.name}: {ex}")

    @classmethod
    def import_enable(self):  # pragma: no cover
        if self._loader is None:
            self._loader = PluginLoader(self)
        self._loader.enable()

    @classmethod
    def import_disable(self):  # pragma: no cover
        if self._loader is not None:
            self._loader.disable()
