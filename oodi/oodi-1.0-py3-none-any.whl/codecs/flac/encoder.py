
from ...codecs.base import BaseEncoder, CommandArgumentParser


class FlacArgumentParser(CommandArgumentParser):
    """
    Argument parser for flac encoding
    """
    pass


class Encoder(BaseEncoder):
    """
    Encoder for FLAC files
    """
    format = 'flac'
    argument_parsers = {
        'flac': FlacArgumentParser(),
    }
