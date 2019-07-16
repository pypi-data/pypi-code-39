__version__ = "1.0.0"

import logging


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


logging.getLogger('core').addHandler(NullHandler())
