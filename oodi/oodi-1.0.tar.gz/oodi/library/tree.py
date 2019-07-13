
import os

from ..codecs.base import Codecs
from ..configuration import Configuration
from ..metadata.base import MetadataLoader

from .base import Directory
from .exceptions import LibraryError
from .track import Track
from .metadata import LibraryJSONMetadata


class Tree(Directory):
    """
    Audio file tree in filesystem

    Audio file tree is a directory prefix containing audio files.

    Formats may be a list of known codec names from oodi.codecs and will limit loading
    of files from tree to files with matching extensions only.
    """

    def __init__(self, path, configuration=None, iterable='files', formats=None, description=None):
        super().__init__(path, configuration=configuration, iterable=iterable)

        self.__metadata_loader__ = MetadataLoader(self.configuration)
        self.metadata_files = []

        self.formats = formats if formats is not None else []
        if isinstance(self.formats, str):
            self.formats = self.formats.split()

        self.description = description

        self.__library_metadata__ = None
        self.__codecs__ = None
        self.__extensions__ = None

    @property
    def metadata(self):
        if self.__library_metadata__ is None:
            self.__library_metadata__ = LibraryJSONMetadata(self)
        return self.__library_metadata__

    @property
    def codecs(self):
        if self.__codecs__ is None:
            self.__codecs__ = Codecs(self.configuration)
        return self.__codecs__

    @property
    def codec(self):
        """
        Return codec used for library

        Raises ValueError if multiple codes match
        """
        if len(self.formats) == 1:
            return getattr(self.codecs, self.formats[0])
        else:
            raise LibraryError('Multiple codecs configured for tree {}'.format(self.path))

    def __load_valid_extensions__(self):
        """
        Load valid filename extensions without leading . based on self.formats value.
        """

        # Only load once, this does not change on the fly
        if self.__extensions__ is not None or not self.formats:
            return

        self.__extensions__ = []
        for format in self.formats:
            codec = getattr(self.codecs, format, None)
            if codec is None:
                raise LibraryError('Unknown codec {} configured for tree {}'.format(self.path, format))
            for extension in codec.extensions:
                if extension not in self.__extensions__:
                    self.__extensions__.append(extension)

    def __validate_extension__(self, filename):
        """
        Validate filename extension against codecs defined by self.formats

        If no formats are specified, all filenames are accepted as valid
        """
        self.__load_valid_extensions__()
        if self.__extensions__ is None:
            return True

        name, extension = os.path.splitext(filename)
        extension = extension.lstrip('.')
        return extension in self.__extensions__

    def add_directory(self, root, directory):
        """
        Add subdirectory to tree
        """
        if directory in self.ignored_tree_folder_names:
            return

        item = Tree(os.path.join(root, directory), configuration=self.configuration, iterable=self.__iterable__)
        self.__directory_index__[item.path] = item
        if root in self.__directory_index__:
            item.parent = self.__directory_index__[root]
        self.directories.append(item)

    def reset(self):
        super().reset()
        self.metadata_files = []

    def add_file(self, root, filename):
        """
        Add audio file to tree

        Only files with supported extensions are loaded.

        If tree specifies self.formats, only files with extension matching codecs are loaded.
        """
        if filename in self.ignored_filenames:
            return

        name, extension = os.path.splitext(filename)
        if self.codecs.find_codecs_for_extension(extension[1:]):
            if self.__validate_extension__(filename):
                item = Track(os.path.join(root, filename), configuration=self.configuration)
                if root in self.__directory_index__:
                    item.parent = self.__directory_index__[root]
                self.files.append(item)

        else:
            loaders = self.__metadata_loader__.find_metadata_type_for_extension(extension[1:])
            if len(loaders) == 1:
                item = loaders[0](os.path.join(root, filename), configuration=self.configuration)
                if root in self.__directory_index__:
                    item.parent = self.__directory_index__[root]
                self.metadata_files.append(item)


class IterableTrackPaths:
    """
    Loader for directories and files as paths, returning always iterable that
    iterates Track objects
    """
    def __init__(self, path, configuration=None):
        if configuration is None:
            configuration = Configuration()
        if os.path.isfile(path):
            self.item = iter([Track(path, configuration=configuration)])
        elif os.path.isdir(path):
            self.item = Tree(path, configuration=configuration)
        else:
            raise LibraryError('Invalid path: {}'.format(path))

    def __iter__(self):
        return self.item
