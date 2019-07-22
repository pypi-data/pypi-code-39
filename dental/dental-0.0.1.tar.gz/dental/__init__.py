try:
    from . import core
    __version__ = core.__version__
except ImportError:
    raise ValueError('The dental core library is not installed correctly.')
