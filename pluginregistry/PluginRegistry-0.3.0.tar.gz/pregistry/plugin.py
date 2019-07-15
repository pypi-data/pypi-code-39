import pkg_resources

from .classproperty import classproperty
from .registry import Registry


class Plugin:
    """
    Plugin base class with automatic registration.
    """

    _registry = None

    @classproperty
    def is_registry(self):
        return False

    @classproperty
    def is_plugin(self):
        return True

    @classmethod
    def __init_subclass__(cls, registry: Registry, **kw):
        super().__init_subclass__(**kw)

        # Plugin Registration
        cls._registry = registry

        if registry is not None:
            cls._registry._plugins[cls.__name__] = cls

    @classproperty
    def registry(cls) -> Registry:
        """
        The registry this plugin will register itself with on request
        """
        return cls._registry

    @classproperty
    def path(cls):
        if cls.registry is None:
            return cls.__name__
        else:
            return f"{cls.registry.path}.{cls.__name__}"

    @classproperty
    def entry_point(cls):
        if cls._registry is not None:
            try:
                dist = pkg_resources.get_distribution(cls.__module__.split(".")[0])
            except pkg_resources.DistributionNotFound:
                dist = None

            return pkg_resources.EntryPoint(
                cls.path, cls.__module__, (cls.__name__,), dist=dist
            )

    def enable(self) -> bool:
        """
        This method will be called to enable the plugin.

        All initialization code should occur here, including any initialization which
        ordinarily would occur in the __init__() method.

        This method must be callable multiple times if a plugin is disabled and enabled
        more than once in a session.
        """

    def disable(self):
        """
        This method is used to disable the plugin.

        All cleanup code should occur here, including any code which ordinarily
        would occur in the __del__() method.

        This method must be callable multiple times if a plugin is disabled and enabled
        more than once in a session.
        """

    def __str__(self):  # pragma: no cover
        return f"<Plugin with entry point [{self.entry_point}]>"
