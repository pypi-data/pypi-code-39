
import os
from ..configuration import ConfigurationSection

DEFAULT_CONFIGURATION = {}


class CodecConfiguration(ConfigurationSection):
    """
    Configuration for codecs
    """
    defaults = os.path.join(os.path.dirname(__file__), 'defaults.yaml')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__codecs__ = None

    @property
    def codecs(self):
        if not self.__codecs__:
            from .base import Codecs
            self.__codecs__ = Codecs(self.configuration)
        return self.__codecs__

    def find_codecs_for_extension(self, extension):
        """
        Return codecs that match specified extension

        May return multiple (.m4a for AAC and ALAC, for example)
        """
        return [codec for codec in self.codecs if extension in codec.extensions]
