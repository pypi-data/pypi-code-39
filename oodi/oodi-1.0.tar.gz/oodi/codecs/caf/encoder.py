
from ...codecs.base import BaseEncoder, CommandArgumentParser


class AFConvertArguments(CommandArgumentParser):
    """
    Default arguments to encode CAF with afconvert
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
    Encoder for CAF files
    """
    format = 'caf'
    argument_parsers = {
        'afconvert': AFConvertArguments(),
    }
