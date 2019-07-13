
import os

from ..configuration import ConfigurationSection


class LibraryConfiguration(ConfigurationSection):
    """
    Configuration for libraries
    """
    defaults = os.path.join(os.path.dirname(__file__), 'defaults.yaml')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__libraries__ = None

    @property
    def libraries(self):
        if not self.__libraries__:
            from .base import Libraries
            self.__libraries__ = Libraries(configuration=self.configuration)
        return self.__libraries__

    def find_tree_by_prefix(self, path):
        """
        Return tree that matches specified extension

        May return multiple (.m4a for AAC and ALAC, for example)
        """
        return self.libraries.find_tree_by_prefix(path)
