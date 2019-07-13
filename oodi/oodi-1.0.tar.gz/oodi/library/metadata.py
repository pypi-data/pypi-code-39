
import json
import os
from datetime import datetime
from operator import itemgetter

from .exceptions import LibraryError

LIBRARY_METADATA_FILENAME = '.metadata.json'


class LibraryFileJSONMetadata:
    """
    Common base class for library file item JSON metadata presentation
    """
    def __init__(self, tree, item):
        self.tree = tree
        self.item = item

        self.__data__ = {}
        self.__loaded__ = False

        if self.tree is not None:
            tree_root = '{}/'.format(self.tree.path)
            if item.path[:len(tree_root)] == tree_root:
                self.filename = item.path[len(tree_root):]
            else:
                self.filename = item.path
        else:
            self.filename = item.path

    @property
    def modified(self):
        return self.item.mtime

    @property
    def data(self):
        if not self.__loaded__:
            self.load()
        return self.__data__

    def keys(self, *args, **kwargs):
        return self.data.keys(*args, **kwargs)

    def values(self, *args, **kwargs):
        return self.data.values(*args, **kwargs)

    def items(self, *args, **kwargs):
        return self.data.items(*args, **kwargs)

    def load(self):
        """
        Load metadata file details to self.__data__
        """
        self.__data__ = {
            'filename': self.filename,
            'magic': self.item.magic,
            'uid': self.item.uid,
            'gid': self.item.gid,
            'modified': self.item.mtime,
            'size_kb': self.item.size,
            'mode': '{:o}'.format(self.item.mode),
            'sha256': self.item.sha256,
        }
        self.__loaded__ = True


class AlbumartJSONMetadata(LibraryFileJSONMetadata):
    """
    Metadata details for a metadata file in library
    """

    def load(self):
        """
        Load track details to self.__data__
        """
        super().load()
        self.__data__['info'] = self.item.info


class TrackJSONMetadata(LibraryFileJSONMetadata):
    """
    Metadata for a track in library
    """

    def load(self):
        """
        Load track details to self.__data__
        """
        super().load()

        tags = self.item.tags
        if tags:
            self.__data__['info'] = tags.info
            self.__data__['tags'] = tags.items()

            if tags.has_albumart:
                albumart = tags.get_albumart()
                if albumart:
                    self.__data__['albumart'] = albumart.info
                else:
                    self.__data__['albumart'] = {}


class LibraryJSONMetadata(dict):
    """
    JSON metadata file for library tree
    """

    def __init__(self, tree, filename=LIBRARY_METADATA_FILENAME):
        self.tree = tree
        self.path = os.path.join(tree.path, filename)

        self.__loaded__ = False
        self['tracks'] = {}
        self['albumarts'] = {}

    def __repr__(self):
        return '{} metadata'.format(self.tree)

    @property
    def track_filenames(self):
        """
        Return track filenames as sortd list
        """
        return sorted(
            track['filename']
            for track in self['tracks'].values()
            if 'filename' in track
        )

    @property
    def albumart_filenames(self):
        """
        Return albumart filenames as sortd list
        """
        return sorted(
            albumart['filename']
            for albumart in self['albumarts'].values()
            if 'filename' in albumart
        )

    @property
    def tracks(self):
        """
        Return tracks from self['tracks'] as list sorted by filename
        """
        return sorted(self['tracks'].values(), key=itemgetter('filename'))

    @property
    def albumarts(self):
        """
        Return album arts from self['albumarts'] as list sorted by filename
        """
        return sorted(self['albumarts'].values(), key=itemgetter('filename'))

    def load(self):
        """
        Load metadata JSON file for library
        """

        self.clear()
        self['tracks'] = {}
        self['albumarts'] = {}

        if not os.path.isfile(self.path):
            return

        try:
            with open(self.path, 'r') as fd:
                data = json.loads(fd.read())
        except Exception as e:
            raise LibraryError('Error loading metadata file {}: {}'.format(self.path, e))

        # Tree root path
        tree_root = '{}/'.format(self.tree.path)

        # Old format
        if type(data) == list:
            for item in data:
                if item['filename'][:len(tree_root)] == tree_root:
                    item['filename'] = item['filename'][len(tree_root):]
                self['tracks'][item['filename']] = item

        # New format with as dict
        elif type(data) == dict:
            for item in data.get('tracks', []):
                if item['filename'][:len(tree_root)] == tree_root:
                    item['filename'] = item['filename'][len(tree_root):]
                self['tracks'][item['filename']] = item

            for item in data.get('albumarts', []):
                if item['filename'][:len(tree_root)] == tree_root:
                    item['filename'] = item['filename'][len(tree_root):]
                self['albumarts'][item['filename']] = item

    def save(self):
        """
        Save metadata to JSON
        """

        if not self.tracks:
            return

        data = json.dumps(
            {
                'tracks': self.tracks,
                'albumarts': self.albumarts,
                'updated': datetime.now().strftime('%s')
            },
            indent=2
        )

        try:
            with open(self.path, 'w') as fd:
                fd.write('{}\n'.format(data))
        except Exception as e:
            raise LibraryError('Error writing metadata file {}: {}'.format(self.path, e))

    def update(self):
        """
        Update metadata for tracks in library tree
        """

        if not self.__loaded__:
            self.load()

        track_filenames = self.track_filenames
        albumart_filenames = self.albumart_filenames

        detected_track_filenames = []
        for track in self.tree:
            item = TrackJSONMetadata(self.tree, track)
            if item.filename in track_filenames:
                if self['tracks'][item.filename]['modified'] < track.mtime:
                    print('UPDATE {}'.format(item.filename))
                    self['tracks'][item.filename] = item.data
            else:
                print('ADD    {}'.format(item.filename))
                self['tracks'][item.filename] = item.data
            detected_track_filenames.append(item.filename)

        detected_albumart_filenames = []
        for metadata_file in self.tree.metadata_files:
            item = AlbumartJSONMetadata(self.tree, metadata_file)
            if item.filename in albumart_filenames:
                if self['albumarts'][item.filename]['modified'] < metadata_file.mtime:
                    print('UPDATE {}'.format(item.filename))
                    self['albumarts'][item.filename] = item.data
            else:
                print('ADD    {}'.format(item.filename))
                self['albumarts'][item.filename] = item.data
            detected_albumart_filenames.append(item.filename)

        for filename in self.track_filenames:
            if filename not in detected_track_filenames:
                print('remove obsolete track', filename)
                del self['tracks'][filename]

        for filename in self.albumart_filenames:
            if filename not in detected_albumart_filenames:
                print('remove obsolete albumart', filename)
                del self['albumarts'][filename]
