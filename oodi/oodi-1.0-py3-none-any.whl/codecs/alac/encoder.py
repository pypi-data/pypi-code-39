
from ...codecs.base import BaseEncoder, CommandArgumentParser


class AFConvertArguments(CommandArgumentParser):
    """
    Default arguments to encode ALAC with afconvert
    """
    pass


class Encoder(BaseEncoder):
    """
    Encoder for ALAC files
    """
    format = 'alac'
    argument_parsers = {
        'afconvert': AFConvertArguments(),
    }
