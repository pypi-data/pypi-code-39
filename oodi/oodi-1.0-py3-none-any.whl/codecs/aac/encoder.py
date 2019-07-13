
from ...codecs.base import BaseEncoder, CommandArgumentParser


class AFConvertArguments(CommandArgumentParser):
    """
    Default arguments to encode AAC with afconvert
    """
    defaults = {
        'quality': '127',
        'bitrate': '256000',
    }
    choices = {
        'quality': [str(i) for i in range(0, 128)]
    }
    args = (
        'quality',
        'bitrate',
    )


class Encoder(BaseEncoder):
    """
    Encoder for AAC files
    """
    format = 'aac'
    argument_parsers = {
        'afconvert': AFConvertArguments(),
    }
