from fs.base import FS

from dropboxfs.dropboxfs import DropboxFS
from dropboxfs.tests.test_dropboxfs import TestDropboxFS


def main():
    ts = TestDropboxFS()
    ts.fs = ts.make_fs()
    ts.test_unicode_path()


if __name__ == "__main__":
    main()
