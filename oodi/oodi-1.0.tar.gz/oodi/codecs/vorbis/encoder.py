
from ...codecs.base import BaseEncoder, CommandArgumentParser


class OggEncArguments(CommandArgumentParser):
    """
    Arguments for oggenc
    """
    defaults = {
        'quality': 8,
    }
    args = (
        'quality',
    )


class Encoder(BaseEncoder):
    """
    Encoder for Vorbis files
    """
    format = 'vorbis'
    argument_parsers = {
        'oggenc': OggEncArguments(),
    }

    def __parse_command__(self, **kwargs):
        for attr in ('quality',):
            if kwargs.get(attr, None) is not None:
                kwargs[attr] = getattr(self, attr)
        return super().__parse_command__(**kwargs)
