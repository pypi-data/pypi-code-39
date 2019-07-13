
from ...codecs.base import BaseEncoder, CommandArgumentParser

DEFAULT_BITRATE = 320


class LameArguments(CommandArgumentParser):
    """
    Arguments to encode with lame
    """
    defaults = {
        'bitrate': 320,
    }
    args = (
        'bitrate',
    )


class Encoder(BaseEncoder):
    """
    Encoder for MP3 files
    """
    format = 'mp3'
    argument_parsers = {
        'lame': LameArguments(),
    }
