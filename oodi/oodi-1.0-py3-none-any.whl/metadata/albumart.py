
import requests
import os

from io import BytesIO
from PIL import ImageFile

from ..library.base import File

from .constants import ALBUMART_FILENAMES, ALBUMART_EXTENSIONS

DEFAULT_ARTWORK_FILENAME = 'artwork.jpg'

PIL_EXTENSION_MAP = {
    'JPEG':     'jpg',
    'PNG':      'png',
}

PIL_MIME_MAP = {
    'JPEG':     'image/jpeg',
    'PNG':      'image/png',
}


class AlbumArtError(Exception):
    """
    ERrors processing album art
    """
    pass


class AlbumArt(File):
    """
    Album art files
    """
    extensions = ALBUMART_EXTENSIONS

    def __init__(self, path=None, configuration=None):
        super().__init__(path, configuration=configuration)
        self.__image__ = None
        self.__mimetype__ = None

        if self.path is not None and os.path.isfile(self.path):
            self.load_file(self.path)

    def __str__(self):
        """
        Return image information
        """
        if self.path is not None:
            return self.path
        else:
            return '%(mime)s %(bytes)d bytes %(width)dx%(height)d' % self.info

    def __len__(self):
        """
        Returns PIL image length as string
        """

        if not self.is_loaded:
            return 0
        return len(self.__image__.tobytes())

    def __parse_image_data__(self, data):
        """
        Load the image from data with PIL
        """

        try:
            parser = ImageFile.Parser()
            parser.feed(data)
            self.__image__ = parser.close()
        except IOError:
            raise AlbumArtError('Error parsing albumart image data')

        try:
            self.__mimetype__ = PIL_MIME_MAP[self.__image__.format]
            if self.__mimetype__ is None:
                raise AlbumArtError('Error detecting image format')
        except KeyError:
            self.__image__ = None
            raise AlbumArtError('Unsupported PIL image format: {}'.format(self.__image__.format))

        if self.__image__.mode != 'RGB':
            self.__image__ = self.__image__.convert('RGB')

    @property
    def exists(self):
        return self.path is not None and os.path.isfile(self.path)

    @property
    def is_loaded(self):
        return self.__image__ is not None

    @property
    def mimetype(self):
        """
        Return file format of loaded album art image
        """
        return self.__mimetype__

    @property
    def file_format(self):
        """
        Return file format of loaded album art image
        """
        if not self.is_loaded:
            raise AlbumArtError('AlbumArt not yet initialized.')
        return self.__image__.format

    @property
    def info(self):
        """
        Return details of loaded album art image
        """
        if not self.is_loaded:
            raise AlbumArtError('AlbumArt not yet initialized.')

        colors = self.__image__.getcolors()
        if colors is None:
            colors = 0

        return {
            'type': 3,  # Album cover
            'mime': self.__mimetype__,
            'bytes': len(self),
            'width': int(self.__image__.size[0]),
            'height': int(self.__image__.size[1]),
            'colors': colors,
        }

    def load_data(self, data):
        """
        Import albumart from metadata tag or database as bytes
        """
        self.__parse_image_data__(data)

    def load_file(self, path):
        """
        Import albumart from file
        """
        if not os.path.isfile(path):
            raise AlbumArtError('No such file: {}'.format(path))
        if not os.access(path, os.R_OK):
            raise AlbumArtError('No permissions to read file: {}'.format(
                path,
            ))

        self.path = path
        with open(path, 'rb') as fd:
            self.__parse_image_data__(fd.read())

    def fetch(self, url):
        """
        Fetch image from URL
        """
        res = requests.get(url)
        if res.status_code != 200:
            raise AlbumArtError('Error fetching url {} (returns {})'.format(url, res.status_code))

        if 'content-type' not in res.headers:
            raise AlbumArtError('Response did not include content type header')

        try:
            content_type = res.headers.get('content-type', None)
            if not content_type:
                raise AlbumArtError('Response missing content-type header')
            prefix, extension = content_type.split('/', 1)
            if prefix != 'image':
                raise AlbumArtError('Content type of data is not supported: {}'.format(content_type))

        except ValueError:
            raise AlbumArtError('Error parsing content type {}'.format(res.headers.get('content-type', None)))

        return self.__parse_image_data__(res.content)

    def dump(self):
        """
        Returns bytes from the image with BytesIO read() call
        """
        if not self.is_loaded:
            raise AlbumArtError('AlbumArt not yet initialized.')

        s = BytesIO()
        self.__image__.save(s, self.file_format)
        s.seek(0)
        return s.read()

    def save(self, path, format=None):
        """
        Saves the image data to given target file.

        If target filename exists, it is removed before saving.
        """
        if not self.is_loaded:
            raise AlbumArtError('AlbumArt not yet initialized.')

        if format is None:
            format = self.file_format

        if os.path.isdir(path):
            path = os.path.join(path, DEFAULT_ARTWORK_FILENAME)

        if os.path.isfile(path):
            try:
                os.unlink(path)
            except IOError as e:
                raise AlbumArtError('Error removing existing file {}: {}'.format(
                    path,
                    e,
                ))

        try:
            self.__image__.save(path, format)
        except IOError as e:
            raise AlbumArtError('Error saving {}: {}'.format(path, e))


def default_album_art(path, configuration=None):
    if os.path.isfile(path):
        path = os.path.dirname(path)

    return AlbumArt('{}/{}'.format(path, DEFAULT_ARTWORK_FILENAME, configuration=configuration))


def detect_album_art(path, configuration=None):
    if os.path.isfile(path):
        path = os.path.dirname(path)

    for filename in ALBUMART_FILENAMES:
        filename = os.path.join(path, filename)
        if os.path.isfile(filename):
            return AlbumArt(filename, configuration=configuration)

    return None
