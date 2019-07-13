
from ...codecs.base import BaseEncoder, CommandArgumentParser


class WavpackConvertArguments(CommandArgumentParser):
    """
    Default arguments to encode wavpack files
    """
    pass


class Encoder(BaseEncoder):
    """
    Encoder for AAC files
    """
    format = 'wavpack'
    argument_parsers = {
        'wavpack': WavpackConvertArguments(),
    }
