#!/usr/bin/env python

import os

from systematic.shell import normalized

from ..library.base import Path


class PlaylistError(Exception):
    pass


class Playlist(list):
    """
    Common base class for playlists
    """

    def __init__(self, name, unique=True):
        self.name = os.path.splitext(os.path.basename(name))[0]
        self.unique = unique
        self.modified = False
        self.path = None

    def __repr__(self):
        return self.path

    def __len__(self):
        if list.__len__(self) == 0:
            self.read()
        return list.__len__(self)

    @property
    def directory(self):
        return self.path.directory

    @property
    def filename(self):
        return self.path.filename

    @property
    def extension(self):
        return self.path.extension

    @property
    def exists(self):
        return self.path.isfile

    def read(self):
        raise NotImplementedError('You must implement reading in subclass')

    def write(self):
        raise NotImplementedError('You must implement writing in subclass')

    def append(self, path, position=None, recursive=False):
        def insert(path, position=None):
            if self.unique and self.count(path) > 0:
                return

            self.modified = True
            if not position:
                super(Playlist, self).append(path)

            else:
                try:
                    position = int(position)
                    if position < 0:
                        raise ValueError

                    if position > list.__len__(self):
                        position = list.__len__(self)

                except ValueError:
                    raise PlaylistError('Invalid position: {}'.format(position))

                self.insert(position, path)

        path = Path(normalized(os.path.realpath(path)))
        if os.path.isfile(path):
            insert(path, position)

        elif os.path.isdir(path):
            for f in ['{}'.format(os.path.join(path, x)) for x in os.listdir(path)]:
                f = Path(normalized(os.path.realpath(f)))

                if not recursive and os.path.isdir(f):
                    continue

                self.append(f, position)

        else:
            raise PlaylistError('Not a file or directory: {}'.format(path))

        self.modified = True


class m3uPlaylist(Playlist):
    def __init__(self, name, config=None, folder=None, unique=True):
        super(m3uPlaylist, self).__init__(name, unique)

        if os.path.isfile(name):
            path = Path(os.path.realpath(name))

        else:
            if folder is not None:
                path = os.path.join(folder, '{}.m3u'.format(self.name))
            else:
                path = os.path.join('{}.m3u'.format(self.name))

        self.path = path

    def read(self):
        if not self.exists:
            return

        try:
            with open(self.path, 'r') as lines:
                self.__delslice__(0, list.__len__(self))
                for line in lines:
                    line = line.strip()
                    if line.startswith('#'):
                        continue

                    filepath = Path(normalized(os.path.realpath(line)))
                    if not os.path.isfile(filepath):
                        continue

                    if self.unique and self.count(filepath) > 0:
                        continue

                    self.append(filepath)
        except IOError as e:
            raise PlaylistError('Error reading {}: {}'.format(self.path, e))

    def write(self):
        pl_dir = os.path.dirname(self.path)

        if not os.path.isdir(pl_dir):
            try:
                os.makedirs(pl_dir)

            except OSError as e:
                raise PlaylistError('Error creating directory {}: {}'.format(pl_dir, e))
            except IOError as e:
                raise PlaylistError('Error creating directory {}: {}'.format(pl_dir, e))

        if not self.modified:
            return

        try:
            fd = open(self.path, 'w')
            for filename in self:
                fd.write('{}\n'.format(filename))
            fd.close()

        except IOError as e:
            raise PlaylistError('Error writing playlist {}: {}'.format(self.path, e))
        except OSError as e:
            raise PlaylistError('Error writing playlist {}: {}'.format(self.path, e))

    def remove(self):
        if not os.path.isfile(self.path):
            return

        try:
            os.unlink(self.path)

        except IOError as e:
            raise PlaylistError('Error removing playlist {}: {}'.format(self.path, e))
        except OSError as e:
            raise PlaylistError('Error removing playlist {}: {}'.format(self.path, e))


class m3uPlaylistDirectory(list):
    def __init__(self, path=None):
        self.path = path
        if not os.path.isdir(self.path):
            raise PlaylistError('No such directory: {}'.format(self.path))

        for item in sorted(os.listdir(self.path)):
            item = Path(os.path.join(self.path, item))

            if path.isfile:
                self.extend(m3uPlaylistDirectory(path=item))
                continue

            if os.path.splitext(item)[1][1:] != 'm3u':
                continue

            self.append(m3uPlaylist(item))

    def __getitem__(self, item):
        try:
            return self[int(item)]
        except IndexError:
            pass
        except ValueError:
            pass

        item = str(item)
        if str(item[-4:]) != '.m3u':
            item += '.m3u'

        try:
            name_lower = item.filename.lower()
            return [item for item in self if item.lower() == name_lower][0]
        except IndexError:
            pass

        try:
            path = os.path.realpath(item)
            return [pl for pl in self if pl.path == path][0]
        except IndexError:
            pass

        raise IndexError('Invalid m3uPlaylistDirectory index {}'.format(item))

    def relative_path(self, item):
        if hasattr(item, 'path'):
            return self.path.relative_path(item.path)
        else:
            return self.path.relative_path(item)
