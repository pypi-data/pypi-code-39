
from ...codecs.base import GenericAudioFile

from .decoder import Decoder
from .encoder import Encoder


class Audiofile(GenericAudioFile):
    """
    CAF audio file
    """

    decoder_class = Decoder
    encoder_class = Encoder

    format = 'caf'
    description = 'Core Audio Format'
    extensions = (
        'caf',
    )
    mimetypes = (
        'audio/x-caf',
    )
