
import os

from ..cli import OodiShellCommandParser


class CodecError(Exception):
    """
    Exceptions from codecs and codec commands
    """
    pass


class TagError(Exception):
    """
    Exceptions from tagging commmands
    """
    pass


class AudiofileProcessorBaseClass(OodiShellCommandParser):
    """
    Base class for audio file processors
    """
    format = None
    commands = ()

    def __repr__(self):
        return self.format


class CommandArgumentParser:
    """
    Process command argument defaults
    """
    defaults = {}
    choices = {}
    args = ()

    def __call__(self, callback):
        kwargs = {}
        for arg in self.args:
            value = getattr(callback, arg, None)
            default = self.defaults.get(arg, None)
            value = value if value is not None else default
            if value is not None:
                self.validate(arg, value)
            kwargs[arg] = value
        return kwargs

    def validate(self, arg, value):
        """
        Validator for fields.

        Implement in child class
        """
        if arg in self.choices:
            if value not in self.choices[arg]:
                raise ValueError('Invalid value: {}'.format(value))


class BaseDecoder(AudiofileProcessorBaseClass):
    """
    Base class for audio file decoders
    """
    def commands(self):
        return self.configuration.codecs.get('decoders', {}).get(self.format, [])

    def decode(self, input_file, output_file=None, **kwargs):
        """
        Run decoder for specified file
        """

        if output_file is None:
            output_file = self.configuration.get_temporary_file_path(suffix='.wav')

        kwargs.update({
            'inputfile': input_file,
            'outputfile': output_file,
        })
        args = self.__parse_command__(**kwargs)
        self.execute(args)
        return output_file


class BaseEncoder(AudiofileProcessorBaseClass):
    """
    Base class for audio file encoders
    """
    default_quality = None
    default_bitrate = None

    @property
    def quality(self):
        """
        Quality from configuration or defaults
        """
        return self.configuration.codecs.get(self.format, {}).get('quality', self.default_quality)

    @property
    def bitrate(self):
        """
        Bitrate from configuration or defaults
        """
        return self.configuration.codecs.get(self.format, {}).get('bitrate', self.default_bitrate)

    def commands(self):
        return self.configuration.codecs.get('encoders', {}).get(self.format, [])

    def encode(self, input_file, output_file=None, remove_input_file=True, **kwargs):
        """
        Run encoder for specified file
        """

        if output_file is None:
            output_file = self.configuration.get_temporary_file_path(suffix='.{}'.format(self.format))

        kwargs.update({
            'inputfile': input_file,
            'outputfile': output_file,
        })
        args = self.__parse_command__(**kwargs)
        self.execute(args)

        if remove_input_file:
            os.unlink(input_file)

        return output_file


class BaseTester(AudiofileProcessorBaseClass):
    """
    Base class for audio file testers
    """
    def commands(self):
        return self.configuration.codecs.get('testers', {}).get(self.format, [])

    def test(self, input_file):
        """
        Run format test for specified file
        """
        raise NotImplementedError


class ValueTotalCountTag:
    """
    Value / total count integer pair for data
    """
    def __init__(self, parser, tag):
        self.parser = parser
        self.tag = tag
        self.value = None
        self.total = None

    def set(self, attr, value):
        """
        Set metadata numbering value to local object

        Formats and validates values and calls self.save() for codec specific saving
        """
        try:
            _value, total = [int(x) for x in str(value).split('/', 1)]
            if _value <= 0 or total <= 0:
                raise ValueError('Invalid numbering tag value {}'.format(value))
            self.value = _value
            self.total = total
        except ValueError:
            try:
                value = int(value)
                if value <= 0:
                    raise ValueError
            except Exception:
                raise ValueError('Invalid numbering tag value {}'.format(value))

            if attr == 'value':
                if self.total == 0:
                    self.total = value
                self.value = value
            elif attr == 'total':
                if self.value is None:
                    self.value = self.parser.track_number
                self.total = value

        if self.value is None:
            raise ValueError('Invalid numbering range {}/{}'.format(self.value, self.total))
        if self.total is not None and self.value > self.total:
            raise ValueError('Invalid numbering range {}/{}'.format(self.value, self.total))

        self.save()

    def get(self):
        raise NotImplementedError

    def save(self):
        """
        Save value / total fields to object.

        This must be implemented in child class
        """
        raise NotImplementedError


class BaseTagParser(AudiofileProcessorBaseClass):
    """
    Base class for audio file tagging classes
    """

    format = None
    supports_list_fields = False
    supports_album_art = False
    loader = None
    fields = {}
    internal_fields = ()
    list_tags = ()
    track_numbering_class = ValueTotalCountTag
    disk_numbering_class = ValueTotalCountTag
    track_numbering_tag = None
    disk_numbering_tag = None

    def __init__(self, configuration):
        """
        Open tags for given file
        """
        self.configuration = configuration
        self.__path__ = None
        self.__entry__ = None
        self.track_numbering = self.track_numbering_class(self, self.track_numbering_tag)
        self.disk_numbering = self.disk_numbering_class(self, self.disk_numbering_tag)

        self.__iterator_index__ = None
        self.__iterator_keys__ = []
        self.__iterator_items__ = {}

    def __repr__(self):
        if self.__path__ is not None:
            return '{} {}'.format(self.format, self.__path__)
        else:
            return '{} no file loaded'.format(self.format)

    def __getattr__(self, attr):
        """
        Get tag by name
        """
        try:
            tag_attributes = self.fields[attr]
        except KeyError:
            raise AttributeError

        if self.__entry__.tags is None:
            return None

        for tag_attribute in tag_attributes:
            if tag_attribute in self.__entry__.tags:
                value = self.__entry__.tags[tag_attribute]
                if attr not in self.list_tags and isinstance(value, list):
                    value = value[0]
                return value
        return None

    def __setattr__(self, attr, value):
        """
        Set tag value
        """
        if attr in ('track_number', 'total_tracks', 'disk_number', 'total_disks'):
            self.__update_numbering_tag__(attr, value)
        elif attr in self.fields:
            tag = self.fields[attr][0]
            self.__entry__[tag] = self.__format_tag__(attr, value)
            self.__entry__.save()
        else:
            super().__setattr__(attr, value)

    def __delattr__(self, attr):
        """
        Remove tag from tags
        """
        if attr in self.fields:
            tag = self.fields[attr][0]
            del(self.__entry__[tag])
            self.__entry__.save()

    def __iter__(self):
        return self

    def __next__(self):
        if self.__iterator_index__ is None:
            self.__iterator_index__ = 0
            self.__iterator_items__ = self.items()
            self.__iterator_keys__ = sorted(key for key in self.__iterator_items__)

        try:
            tag = self.__iterator_keys__[self.__iterator_index__]
            value = self.__iterator_items__[self.__iterator_keys__[self.__iterator_index__]]
            self.__iterator_index__ += 1
            return (tag, value)
        except IndexError:
            self.__iterator_index__ = None
            raise StopIteration

    def __update_numbering_tag__(self, tag, value):
        """
        Update value / total disk numbering tags
        """
        if tag == 'track_number':
            self.track_numbering.set('value', value)
        elif tag == 'total_tracks':
            self.track_numbering.set('total', value)
        elif tag == 'disk_number':
            self.disk_numbering.set('value', value)
        elif tag == 'total_disks':
            self.disk_numbering.set('total', value)

    def __format_tag__(self, tag, value):
        """
        Format tag to internal tag presentation
        """
        return value

    @property
    def file_loaded(self):
        """
        Return true if tags have been loaded with a file
        """
        return self.__path__ is not None

    @property
    def track_number(self):
        try:
            self.track_numbering.get()
        except NotImplementedError:
            raise CodecError('{} track numbering not implemented'.format(self.__class__))
        return self.track_numbering.value

    @property
    def total_tracks(self):
        try:
            self.track_numbering.get()
        except NotImplementedError:
            raise CodecError('{} track numbering not implemented'.format(self.__class__))
        return self.track_numbering.total

    @property
    def disk_number(self):
        try:
            self.disk_numbering.get()
        except NotImplementedError:
            raise CodecError('{} disk numbering not implemented'.format(self.__class__))
        return self.disk_numbering.value

    @property
    def total_disks(self):
        try:
            self.disk_numbering.get()
        except NotImplementedError:
            raise CodecError('{} disk numbering not implemented'.format(self.__class__))
        return self.disk_numbering.total

    @property
    def info(self):
        """
        Return information about loaded file
        """
        if self.__path__:
            return vars(self.__entry__.info)
        else:
            return {}

    def load(self, path):
        """
        Load tags for audio file
        """
        self.__path__ = path
        self.__entry__ = self.loader(os.path.expandvars(os.path.expanduser(path)))

    def update(self, **kwargs):
        """
        Update tags from kwargs

        TODO - now we set tags one by one and save, do it more efficiently
        """

        if 'track_number' in kwargs and 'total_tracks' in kwargs:
            kwargs['track_number'] = '{}/{}'.format(kwargs['track_number'], kwargs['total_tracks'])
            del kwargs['total_tracks']

        for tag, value in kwargs.items():
            setattr(self, tag, value)

    def items(self, internal_fields=False):
        """
        Get all known tags
        """
        items = {}
        for field in self.fields.keys():
            if field in self.internal_fields and not internal_fields:
                continue

            value = self.__getattr__(field)
            if value is not None:
                items[field] = value

        for attr in ('track_number', 'total_tracks', 'disk_number', 'total_disks'):
            value = getattr(self, attr, None)
            if value is not None:
                items[attr] = value

        return items

    def has_albumart(self):
        """
        Check if file has album art tag
        """
        raise NotImplementedError('has_albumart must be defined in child class')

    def get_albumart(self):
        """
        Return album art from tags
        """
        raise NotImplementedError('get_albumart must be defined in child class')

    def set_albumart(self, albumart):
        """
        Embed albumart to audio file
        """
        raise NotImplementedError('set_albumart must be defined in child class')

    def save_albumart(self, path):
        """
        Return album art from tags to a file
        """
        albumart = self.get_albumart()
        if albumart:
            albumart.save(path)
        else:
            raise TagError('No albumart detected in file')
        return albumart

class GenericAudioFile(AudiofileProcessorBaseClass):
    """
    Generic audio file base class
    """

    decoder_class = None
    encoder_class = None
    tester_class = None
    tagparser_class = None

    description = None
    extensions = ()
    mimetypes = ()

    @property
    def decoder(self):
        """
        Return decoder for audio file if available
        """
        if self.decoder_class is not None:
            return self.decoder_class(self.configuration)
        else:
            raise CodecError('Codec {} has no decoder'.format(self.format))

    @property
    def encoder(self):
        """
        Return encoder for audio file if available
        """
        if self.encoder_class is not None:
            return self.encoder_class(self.configuration)
        else:
            raise CodecError('Codec {} has no encoder'.format(self.format))

    @property
    def tagparser(self):
        """
        Return tag parsers for audio file if available
        """
        if self.tagparser_class:
            return self.tagparser_class(self.configuration)
        else:
            raise CodecError('Codec {} does not support tagging'.format(self.format))

    @property
    def tester(self):
        """
        Return tester for audio file if available
        """
        if self.tester_class is not None:
            return self.tester_class(self.configuration)
        else:
            raise CodecError('Codec {} does not support testing'.format(self.format))


class Codecs(list):
    """
    Supported codec implementations
    """

    def __init__(self, configuration):
        from .aac.audiofile import Audiofile as AAC
        from .aif.audiofile import Audiofile as AIF
        from .alac.audiofile import Audiofile as ALAC
        from .caf.audiofile import Audiofile as CAF
        from .flac.audiofile import Audiofile as FLAC
        from .mp3.audiofile import Audiofile as MP3
        from .opus.audiofile import Audiofile as OPUS
        from .vorbis.audiofile import Audiofile as VORBIS
        from .wav.audiofile import Audiofile as WAV
        from .wavpack.audiofile import Audiofile as WAVPACK

        self.configuration = configuration
        self.extend([
            AAC(self.configuration),
            AIF(self.configuration),
            ALAC(self.configuration),
            CAF(self.configuration),
            FLAC(self.configuration),
            MP3(self.configuration),
            OPUS(self.configuration),
            VORBIS(self.configuration),
            WAV(self.configuration),
            WAVPACK(self.configuration),
        ])

    def __getattr__(self, name):
        """
        Get codec by name of format
        """
        for codec in self:
            if codec.format == name:
                return codec
        raise AttributeError('No such codec: {}'.format(name))

    def find_codecs_for_extension(self, extension):
        """
        Return codecs that match specified extension

        May return multiple (.m4a for AAC and ALAC, for example)
        """
        return [codec for codec in self if extension in codec.extensions]

    def find_codec_for_filename(self, path):
        """
        Find codec matching filename
        """
        name, extension = os.path.splitext(os.path.basename(path))
        extension = extension.lstrip('.')
        for codec in self:
            if extension not in codec.extensions:
                continue
            return codec
        return None

    def get_tags_for_filename(self, path):
        """

        """
        codec = self.find_codec_for_filename(path)
        if codec:
            tags = codec.tagparser
            path = os.path.realpath(os.path.expandvars(os.path.expanduser(path)))
            if os.path.isfile(path):
                tags.load(path)
            return tags

        return None
