
from ...codecs.base import GenericAudioFile

from .decoder import Decoder
from .encoder import Encoder
from .tagparser import TagParser


class Audiofile(GenericAudioFile):
    """
    MP3 audio file
    """

    decoder_class = Decoder
    encoder_class = Encoder
    tagparser_class = TagParser

    format = 'mp3'
    description = 'MPEG-2 Audio Layer III'
    extensions = (
        'mp3',
    )
    mimetypes = (
        'audio/mpeg',
        'audio/MPA',
        'audio/mpa-robust',
    )
