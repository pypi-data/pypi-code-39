
import hashlib
import magic
import os

from systematic.shell import normalized

from .exceptions import LibraryError
from ..configuration import Configuration


class Path(str):
    """
    Filesystem path item with some extra attributes
    """

    def __new__(self, path):
        return str.__new__(self, normalized(path))

    @property
    def exists(self):
        """
        Checks if path exists
        """
        if os.path.isdir(self) or os.path.isfile(self) or os.path.islink(self):
            return True
        return False

    @property
    def isdir(self):
        """
        Checks if path is directory
        """
        return os.path.isdir(self)

    @property
    def isfile(self):
        """
        Checks if path is file
        """
        return os.path.isfile(self)

    @property
    def islink(self):
        """
        Checks if path is link
        """
        return os.path.isfile(self)

    @property
    def no_ext(self):
        """
        Return path without extension
        """
        return os.path.splitext(self)[0]

    @property
    def directory(self):
        """
        Return parent directory for path
        """
        return os.path.dirname(self)

    @property
    def filename(self):
        """
        Return path filename part
        """
        return os.path.basename(self)

    @property
    def extension(self):
        """
        Return path extension without leading .
        """
        return os.path.splitext(self)[1][1:]

    def relative_path(self, path):
        """Return relative path

        Return item's relative path compared to specified path
        """
        if path[:len(self)] != self:
            raise ValueError('{} path is not relative to {}'.format(path, self))
        return path[len(self):].lstrip('/')


class FilesystemItem:
    """
    Common filesystem item base class
    """

    def __init__(self, path, configuration=None):
        self.configuration = configuration if configuration is not None else Configuration()
        if path is not None:
            path = os.path.expandvars(os.path.expanduser(path))
        self.__checksums__ = {}
        self.path = path

    def __repr__(self):
        return self.path

    def __stat__(self):
        """
        Try to stat item
        """
        try:
            return os.stat(self.path)
        except Exception as e:
            raise LibraryError('Error running stat on {}: {}'.format(self.path, e))

    @property
    def sha256(self):
        if 'sha256' not in self.__checksums__:
            with open(self.path, "rb") as fd:
                self.__checksums__['sha256'] = hashlib.sha256(fd.read()).hexdigest()
        return self.__checksums__['sha256']

    @property
    def uid(self):
        return self.__stat__().st_uid

    @property
    def gid(self):
        return self.__stat__().st_gid

    @property
    def atime(self):
        return self.__stat__().st_atime

    @property
    def ctime(self):
        return self.__stat__().st_ctime

    @property
    def mtime(self):
        return self.__stat__().st_mtime

    @property
    def mode(self):
        return self.__stat__().st_mode

    @property
    def size(self):
        return self.__stat__().st_size


class Directory(FilesystemItem):
    """
    Iterable directory base class
    """

    # Ignore these filesystem metadata names
    ignored_tree_folder_names = (
        '.fseventsd',
        '.Spotlight-V100',
        '.DocumentRevisions-V100',
        '.Trashes',
        '.vol',
        '__pycache__',
    )
    # File extensions always ignored during iterator
    ignored_filenames = (
        '.DS_Store',
    )

    def __init__(self, path, configuration=None, iterable='files'):
        """
        Initialize iterable directory

        Argument iterable must be name of the attribute being iterated, in this implementation
        'directories' or 'files' unless class is extended to do something else.
        """
        super().__init__(path, configuration)

        self.__iterable__ = iterable
        self.reset()

    def __len__(self):
        """
        Return number of iterable items

        May return incomplete value is full tree is not yet loaded
        """
        return len(self.__get_iterable__())

    def __get_iterable__(self):
        """
        Return iterable field from object
        """
        iterable = getattr(self, self.__iterable__, None)
        if iterable is None:
            raise ValueError('Unknown iterable type: {}'.format(self.__iterable__))

        if not isinstance(iterable, list):
            raise ValueError('Attribute {} is not a list'.format(self.__iterable__))

        return iterable

    def __iter__(self):
        return self

    def __load_next__(self):
        """
        Load next iterable item
        """
        def get_next_slice():
            """
            Get next slice from os.walk and add directories / files to tree

            Iterator will raise StopIteration when all is processed.
            """
            try:
                root, dirs, files = next(self.__iterator__)
                dirs.sort()
            except StopIteration:
                self.__file_index__ = None
                self.__loaded__ = True
                raise StopIteration

            if os.path.basename(root) not in self.ignored_tree_folder_names:
                for directory in dirs:
                    self.add_directory(root, directory)
                for filename in sorted(files):
                    self.add_file(root, filename)

        if self.__iterator__ is None:
            self.__iterator__ = os.walk(self.path, followlinks=True)
            self.__file_index__ = 0
            get_next_slice()

        try:
            item = self.__get_iterable__()[self.__file_index__]
        except IndexError:
            get_next_slice()
            return self.__load_next__()

        self.__file_index__ += 1
        return item

    def __next__(self):
        """
        Directory iterator.

        On first round loads directory from disk as generator.

        After that, use directories and files stored to object without reloading.
        """

        if self.__loaded__ is False:
            return self.__load_next__()

        else:
            if self.__file_index__ is None:
                self.__file_index__ = 0

            try:
                item = self.__get_iterable__()[self.__file_index__]
            except IndexError:
                self.__file_index__ = 0
                raise StopIteration

            self.__file_index__ += 1
            return item

    @property
    def exists(self):
        """
        Check if directory exists
        """
        return os.path.isdir(self.path)

    @property
    def relative_path(self):
        """
        Return path relative to root of tree
        """
        if self.parent is not None:
            root = self.parent
            while True:
                if root.parent:
                    root = root.parent
                else:
                    break
            return self.path[len(root.path) + 1:]
        else:
            return ''

    def add_directory(self, root, directory):
        """
        Add directory to tree if valid.

        Override in child class as necessary.
        """
        if directory in self.ignored_tree_folder_names:
            return

        item = Directory(os.path.join(root, directory), configuration=self.configuration, iterable=self.__iterable__)
        self.__directory_index__[item.path] = item
        if root in self.__directory_index__:
            item.parent = self.__directory_index__[root]
        self.directories.append(item)

    def add_file(self, root, filename):
        """
        Add file to tree if valid.

        Override in child class as necessary.
        """
        if filename in self.ignored_filenames:
            return

        item = File(os.path.join(root, filename, configuration=self.configuration))
        if root in self.__directory_index__:
            item.parent = self.__directory_index__[root]
        self.files.append(item)

    def reset(self):
        """
        Reset loaded data to empty defaults
        """

        self.__directory_index__ = {self.path: self}
        self.parent = None
        self.directories = []
        self.files = []

        self.__loaded__ = False
        self.__iterator__ = None
        self.__file_index__ = None

    def load(self):
        """
        Load all items in the tree instead of iterating
        """
        self.reset()

        while True:
            try:
                next(self)
            except StopIteration:
                break


class File(FilesystemItem):
    """
    File in library
    """
    pass

    @property
    def magic(self):
        """
        Return file magic string
        """
        try:
            with magic.Magic() as m:
                return m.id_filename(self.path)
        except Exception:
            return ''


class Libraries:
    """
    Loader for configured libraries
    """

    def __init__(self, configuration=None):
        self.configuration = configuration if configuration is not None else Configuration()
        self.trees = []
        self.__initialize_trees__()

        self.__iter_index__ = None
        self.__iter_keys__ = []

    def __initialize_trees__(self):
        """
        Return configured trees
        """
        for item in self.configuration.library.get('trees', []):
            prefixes = item.get('prefixes', [])
            if prefixes:
                # Load directories matching prefixes
                for path in prefixes:
                    path = os.path.realpath(os.path.expandvars(os.path.expanduser(path)))
                    if os.path.isdir(path):
                        self.add_tree(
                            path,
                            formats=item.get('formats', None),
                            description=item.get('description', None),
                        )
            elif item.get('path', None):
                self.add_tree(
                    item['path'],
                    formats=item.get('formats', None),
                    description=item.get('description', None),
                )

    def __iter__(self):
        return self

    def __next__(self):
        if self.__iter_index__ is None:
            self.__iter_index__ = 0
            self.__iter_keys__ = self.trees
        try:
            tree = self.trees[self.__iter_index__]
            self.__iter_index__ += 1
            return tree
        except IndexError:
            raise StopIteration

    def add_tree(self, path, description=None, formats=list):
        """
        Add tree to libraries configuration
        """
        from oodi.library.tree import Tree

        for item in self.trees:
            if item.path == path:
                raise LibraryError('Tree already in library: {}'.format(path))

        self.trees.append(Tree(
            path,
            configuration=self.configuration,
            iterable='files',
            formats=formats,
            description=description,
        ))

    def remove_tree(self, path):
        """
        Remove tree from libraries configuration

        Does not remove any directorieos or files in filesystem
        """
        matches = []
        for tree in self.trees:
            if tree.path == path:
                matches.append(tree)
                self.trees.remove(tree)

        if not matches:
            raise LibraryError('Tree was found not in library: {}'.format(path))

    def find_tree_by_prefix(self, path):
        """
        Return tree matching specified prefix
        """
        path = os.path.realpath(os.path.expandvars(os.path.expanduser(path)))
        for tree in self.trees:
            prefix = '{}/'.format(tree.path)
            if tree.path == path or path[:len(prefix)] == prefix:
                return tree

    def find_trees_by_codec(self, name):
        """
        Find trees matching specified codec name

        Multiple trees may be returned
        """
        trees = []
        for tree in self.trees:
            if name in tree.formats:
                trees.append(tree)
        return trees
