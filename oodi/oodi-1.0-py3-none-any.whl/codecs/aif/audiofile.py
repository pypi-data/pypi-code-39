
from ...codecs.base import GenericAudioFile

from .decoder import Decoder
from .encoder import Encoder
from .tagparser import TagParser


class Audiofile(GenericAudioFile):
    """
    AIF audio file
    """

    decoder_class = Decoder
    encoder_class = Encoder
    tagparser_class = TagParser

    format = 'aif'
    description = 'Audio Interchange File Format'
    extensions = (
        'aif',
        'aiff',
        'aifc',
    )
    mimetypes = (
        'audio/x-aiff',
        'audio/aiff',
    )
