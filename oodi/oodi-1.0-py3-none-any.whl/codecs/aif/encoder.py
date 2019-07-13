
from ...codecs.base import BaseEncoder, CommandArgumentParser


class AFConvertArguments(CommandArgumentParser):
    """
    Default arguments to encode AIFF with afconvert
    """
    defaults = {
        'sample_bits': '16',
    }
    choices = {
        'sample_bits': ['16', '24', '32']
    }
    args = (
        'sample_bits',
    )


class Encoder(BaseEncoder):
    """
    Encoder for AIFF files
    """
    format = 'aif'
    argument_parsers = {
        'afconvert': AFConvertArguments(),
    }
