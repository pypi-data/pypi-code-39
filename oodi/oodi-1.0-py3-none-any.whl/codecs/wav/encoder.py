
from ...codecs.base import BaseEncoder, CommandArgumentParser


class AFConvertArguments(CommandArgumentParser):
    """
    Default arguments to encode WAV with afconvert
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
    Encoder for WAV files
    """
    format = 'wav'
    argument_parsers = {
        'afconvert': AFConvertArguments(),
    }
