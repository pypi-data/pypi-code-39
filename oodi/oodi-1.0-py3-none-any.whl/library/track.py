
import os
import re
import tempfile

from .base import File
from .exceptions import LibraryError
from .metadata import TrackJSONMetadata

# Regexp patterns to match track filenames
TRACKNAME_PATTERNS = (
    r'(?P<track_number>\d+)/(?P<total_tracks>\d+) (?P<name>.*)\.(?P<extension>[\w\d]+)$',
    r'(?P<track_number>\d+) (?P<name>.*)\.(?P<extension>[\w\d]+)$',
    r'(?P<name>.*)\.(?P<extension>[\w\d]+)$',
)

ITUNES_BROKEN_AAC_MAGIC = 'ISO Media, MP4 v2 [ISO 14496-14]'
ITUNES_EXPECTED_AAC_MAGIC = 'ISO Media, Apple iTunes ALAC/AAC-LC (.M4A) Audio'


class Track(File):
    """
    Audio file track in tree
    """

    def __init__(self, *args, **kwargs):
        self.format = kwargs.pop('format', None)
        super().__init__(*args, **kwargs)

        self.track_number = None
        self.total_tracks = None
        self.name = None
        self.extension = None
        self.__parse_details_from_filename__()

        self.__metadata__ = None
        self.__tagparser__ = None
        self.__tree__ = None

    def __parse_details_from_filename__(self):
        """
        Parse track details from filename
        """

        patterns = [re.compile(pattern) for pattern in TRACKNAME_PATTERNS]
        directory = os.path.dirname(self.path)
        filename = os.path.basename(self.path)

        for pattern in patterns:
            m = pattern.match(filename)
            if m:
                for attr, value in m.groupdict().items():
                    if attr == 'track_number':
                        value = int(value)
                    setattr(self, attr, value)
                break

        # Guess number of total tracks in directory
        if self.total_tracks is None:
            total_tracks = 0
            for filename in os.listdir(directory):
                if os.path.splitext(filename)[1][1:] == self.extension:
                    total_tracks += 1
            self.total_tracks = total_tracks

    @property
    def tree(self):
        """
        Find library tree based on path
        """
        if self.__tree__ is None:
            self.__tree__ = self.configuration.library.find_tree_by_prefix(self.path)
        return self.__tree__

    @property
    def metadata(self):
        if self.__metadata__ is None:
            self.__metadata__ = TrackJSONMetadata(self.__tree__, self)
        return self.__metadata__

    @property
    def relative_path(self):
        """
        Return relative path to library

        Raises LibraryError if file is not linked to a tree
        """
        if self.tree is not None:
            prefix = '{}/'.format(self.tree.path)
            return self.path[len(prefix):].lstrip('/')
        else:
            raise LibraryError('File {} is not linked to a tree'.format(self.path))

    @property
    def codec(self):
        """
        Get codec for file based on filename extension
        """
        from oodi.codecs.utils import detect_file_codec
        if self.format:
            codecs = self.configuration.codecs.codecs
            for codec in codecs:
                if codec.format == self.format:
                    return codec
            raise LibraryError('Unknown format: {}'.format(self.format))
        elif self.extension:
            codecs = self.configuration.codecs.find_codecs_for_extension(self.extension)
            if len(codecs) == 1:
                return codecs[0]
            else:
                tree = self.tree
                if tree is not None:
                    return tree.codec
                else:
                    self.format = detect_file_codec(self.path)
                    if self.format is not None:
                        codecs = self.configuration.codecs.codecs
                        for codec in codecs:
                            if codec.format == self.format:
                                return codec
                    raise LibraryError('Extension {} matches multiple codecs'.format(self))
        else:
            raise LibraryError('Filename has no extension:{}'.format(self.path))

    @property
    def supports_tags(self):
        """
        Boolean flag to check if format supports tagging
        """
        return self.codec.tagparser_class is not None

    @property
    def tags(self):
        if self.__tagparser__ is None:
            self.__tagparser__ = self.codec.tagparser
            self.__tagparser__.load(self.path)
        return self.__tagparser__

    @property
    def length(self):
        """
        Return length of file as float
        """
        return self.tags.info['length']

    @property
    def bitrate(self):
        """
        Return file bitrate as integer
        """
        return self.tags.info['bitrate']

    @property
    def channels(self):
        """
        Return number of audio channels
        """
        return self.tags.info['channels']

    @property
    def bits_per_sample(self):
        """
        Return file sample bit depth (16, 24 etc)
        """
        for attr in ('bits_per_sample', 'sample_size'):
            if attr in self.tags.info:
                return self.tags.info[attr]
        return None

    @property
    def sample_rate(self):
        """
        Return file sample rate (44100, 48000 etc)
        """
        return self.tags.info['sample_rate']

    def decode(self, output_file=None, *args, **kwargs):
        """
        Decode file to specified output file
        """
        decoder = self.codec.decoder
        if decoder:
            return decoder.decode(self.path, output_file, *args, **kwargs)
        else:
            raise LibraryError('Codec has no decoder')

    def encode(self, input_file, *args, **kwargs):
        """
        Encode specified file to track path
        """
        encoder = self.codec.encoder
        if encoder:
            return encoder.encode(input_file, self.path, *args, **kwargs)
        else:
            raise LibraryError('Codec has no encoder')

    def test(self, *args, **kwargs):
        """
        Run format tester for file
        """
        tester = self.codec.tester
        if tester:
            return tester.test(self.path, *args, **kwargs)
        else:
            raise LibraryError('Codec has no format tester')

    def requires_aac_itunes_fix(self):
        return self.magic == ITUNES_BROKEN_AAC_MAGIC

    def fix_aac_for_itunes(self):
        """
        Fix old AAC files for itunes

        Old files no more playing have magic 'ISO Media, MP4 v2 [ISO 14496-14]'
        """
        from shutil import copyfile
        from subprocess import check_output

        magic = self.magic
        # Already correct magic
        if magic == ITUNES_EXPECTED_AAC_MAGIC:
            return

        # Check this is actually of broken type
        if magic != ITUNES_BROKEN_AAC_MAGIC:
            return

        # Get tag items to process to be added back to corrected file
        tags = self.tags.items()

        # Get album art
        albumart = self.tags.get_albumart()

        tmpdir = tempfile.mkdtemp(prefix='oodi-')
        broken = '{}/broken.m4a'.format(tmpdir)
        fixed = '{}/fixed.m4a'.format(tmpdir)

        # Copy file to /tmp for processing
        copyfile(self.path, broken)

        # Use afconvert to create new file. This will have correct container type
        check_output((
            'afconvert',
            '-b', '256000',
            '-f', 'm4af',
            '-d', 'aac',
            '--soundcheck-generate',
            broken,
            fixed,
        ))

        # Add existing tags back to fixed file
        self.tags.load(fixed)
        self.tags.update(**tags)

        # Embed album art
        if albumart is not None:
            self.tags.set_albumart(albumart)

        # Copy fixed file back in place
        copyfile(fixed, self.path)

        try:
            os.unlink(broken)
            os.unlink(fixed)
            os.rmdir(tmpdir)
        except Exception:
            pass
