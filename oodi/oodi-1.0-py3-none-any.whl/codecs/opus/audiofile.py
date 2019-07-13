
from ...codecs.base import GenericAudioFile

from .decoder import Decoder
from .encoder import Encoder
from .tagparser import TagParser


class Audiofile(GenericAudioFile):
    """
    Opus audio file
    """

    decoder_class = Decoder
    encoder_class = Encoder
    tagparser_class = TagParser

    format = 'opus'
    description = 'Opus (RFC 6716)'
    extensions = (
        'opus',
    )
    mimetypes = (
        'audio/opus',
        'audio/ogg',
    )
