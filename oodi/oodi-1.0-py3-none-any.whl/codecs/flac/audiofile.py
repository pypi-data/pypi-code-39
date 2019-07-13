
from ...codecs.base import GenericAudioFile

from .decoder import Decoder
from .encoder import Encoder
from .tagparser import TagParser


class Audiofile(GenericAudioFile):
    """
    FLAC audio file
    """

    decoder_class = Decoder
    encoder_class = Encoder
    tagparser_class = TagParser

    format = 'flac'
    description = 'Free Lossless Audio Codec'
    extensions = (
        'flac',
    )
    mimetypes = (
        'audio/flac',
    )
