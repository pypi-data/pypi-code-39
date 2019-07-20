"""Init"""


class Config:
    def __init__(self):
        if "config" not in self.__dict__:
            self.config = dict()

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value

    def get(self, key):
        return self.config[key]

    def update(self, iterable):
        self.config.update(iterable)

    def add(self, key, value):
        self.config[key] = value


class RenderConfig(Config):
    """The Rendering configuration implemented with Borg Patten"""

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        super().__init__()


class PrinterConfig(Config):
    """The printer configuration implemented with Borg Pattern"""

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        super().__init__()


class MapConfig(Config):
    """The map configuration implemented with Borg Pattern"""

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        super().__init__()


__version__ = "1.0.0"
