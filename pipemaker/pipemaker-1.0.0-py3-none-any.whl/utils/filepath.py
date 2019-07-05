import fs
import fs.path
from fs.opener.parse import parse_fs_url
import importlib

import logging
log = logging.getLogger()

class Filepath:
    """ wraps pyfilesystem url
    """

    def __init__(self, url):
        """ convert url into root and path"""

        # default filesystem
        if "://" not in url:
            url = f"osfs://{url}"

        # parse url. note parse_result.path appears to be unused
        parse_result = parse_fs_url(url)
        protocol  = parse_result.protocol.lower()
        self.path = parse_result.resource
        self.root = f"{protocol}://"

        # s3 root must include bucket
        if protocol=="s3":
            # parts is ["./", bucket, path, to, file]
            parts = fs.path.parts(self.path)
            self.root = f"{self.root}{parts[1]}"
            self.path = fs.path.join(*parts[2:])

        # windows root must include drive
        elif protocol=="osfs":
            res = self.path.split(":/")
            if len(res)==1:
                pass
            elif len(res)==2:
                self.root = f"{self.root}{res[0]}:/"
                self.path = res[1]
            else:
                raise Exception("invalid path")

    @property
    def fs(self):
        """ return open filesystem """
        # must be here rather than __init__ as cannot be pickled
        return fs.open_fs(self.root)

    @property
    def url(self):
        return f"{self.root}{self.path}"

    @property
    def varname(self):
        """ return just the variable name for simple display """
        filename = fs.path.basename(self.path)
        return fs.path.splitext(filename)[0]

    def __repr__(self):
        return self.url

    def __str__(self):
        return self.varname

    def __hash__(self):
        """ unique key for dict """
        return hash(repr(self))

    def __eq__(self, other):
        return repr(self)==repr(other)

    def __getattr__(self, item):
        """ shortcut for functions with signature filepath.fs.func(path)
        other funcs need to be defined explicitly or use filepath.fs(*args)
        """
        # lambda means call filepath.remove() rather than filepath.remove
        return lambda: getattr(self.fs, item)(self.path)

    def load(self):
        """ return file contents. use extension to determine driver """
        ext = fs.path.splitext(self.path)[-1] or ".pkl"
        try:
            i = importlib.import_module(f"pipemaker.drivers{ext}")
        except ModuleNotFoundError:
            log.error(f"No driver found for extension {ext}. You can add one in the drivers folder.")
            raise
        return i.load(self)

    def save(self, obj):
        """ save obj to file. use extension to determine driver """
        saved_path = self.path
        try:
            # save file using driver selected based on extension
            ext = fs.path.splitext(self.path)[-1] or ".pkl"
            try:
                i = importlib.import_module(f"pipemaker.drivers{ext}")
            except ModuleNotFoundError:
                log.error(f"No driver found for extension {ext}. You can add one in the drivers folder.")
                raise

            # save to temp file so file is not visible until complete.
            dirname, filename = fs.path.split(self.path)
            temp_dir = f"{dirname}/temp"
            self.fs.makedirs(temp_dir, recreate=True)
            self.path = f"{temp_dir}/{filename}"
            i.save(self, obj)

            # move temp file to target location
            self.fs.move(f"{self.path}", f"{saved_path}", overwrite=True)
            if self.fs.isempty(temp_dir):
                self.fs.removedir(temp_dir)
        except Exception:
            log.exception(f"Problem saving {self.url}")
            raise
        finally:
            # restore original path
            self.path = saved_path
