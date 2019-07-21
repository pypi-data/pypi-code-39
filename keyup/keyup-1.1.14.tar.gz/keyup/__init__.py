from keyup._version import __version__ as version


__author__ = 'Blake Huber'
__version__ = version
__email__ = "blakeca00@gmail.com"


# ---  ancillary modules below line -------------------------------------------


from keyup import logd
logger = logd.getLogger(__version__)
