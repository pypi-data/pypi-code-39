import os
from pathlib import Path

import pytest

_temp_dir = None
_resources = {}
_remfile_dirs = []


@pytest.hookimpl
def pytest_collection_finish(session):
    from pathlib import Path
    import tempfile

    global _temp_dir
    _temp_dir = Path(tempfile.mkdtemp())

    global _resources
    for item in session.items:
        for mark in item.iter_markers("remfiles"):
            for uri in list(mark.args[0]):
                filename = _filename(uri)
                uri = _normalize_uri(uri)
                store_filepath = _temp_dir / _hash(uri)
                _resources.update(
                    {uri: {"filename": filename, "store_filepath": store_filepath}}
                )


@pytest.hookimpl
def pytest_sessionfinish(session, exitstatus):
    import shutil

    global _temp_dir
    if _temp_dir is not None and _temp_dir.exists():
        shutil.rmtree(_temp_dir)


@pytest.hookimpl
def pytest_runtest_teardown(item, nextitem):
    global _remfile_dirs

    for r in _remfile_dirs:
        r.cleanup()

    return nextitem


@pytest.hookimpl
def pytest_configure(config):
    config.addinivalue_line("markers", "remfiles(uris): mark test to use a remote file")


@pytest.fixture
def remfiles(request, tmpdir):
    global _resources

    uris = []
    for mark in request.node.iter_markers("remfiles"):
        for uri in list(mark.args[0]):
            uri = _normalize_uri(uri)
            if uri not in _resources:
                msg = f"<{uri}> has been requested but had not been collected."
                raise RuntimeError(msg)
            uris.append(uri)

    uris = set(uris)
    _fetch_files(uris)
    _copy_files([_resources[uri] for uri in uris], tmpdir)

    o = RemFilesDir(tmpdir)
    global _remfile_dirs
    _remfile_dirs.append(o)
    return o


class RemFilesDir:
    def __init__(self, newpath: Path):
        self._newpath = newpath
        self._oldpath = Path(os.getcwd())

    def chdir(self):
        self._newpath.chdir()

    def cleanup(self):
        import shutil

        os.chdir(self._oldpath)
        if self._newpath.exists():
            shutil.rmtree(self._newpath)


def _copy_files(file_items, dst_dir):
    import shutil

    for f in file_items:
        src = f["store_filepath"]
        dst = dst_dir / f["filename"]
        shutil.copy2(src, dst)


def _fetch_files(uris):
    global _temp_dir
    global _resources

    for uri in uris:
        filepath = _resources[uri]["store_filepath"]
        if not filepath.exists():
            _download(uri, filepath)


def _filename(url: str):
    import os
    from urllib.parse import urlparse

    a = urlparse(url)
    return os.path.basename(a.path)


def _hash(x: str):
    import hashlib

    return hashlib.sha1(x.encode()).hexdigest()


def _download(uri, filepath: Path):
    from urllib.request import urlretrieve
    from urllib.error import HTTPError

    tries = 3
    while tries > 0:
        try:
            urlretrieve(uri, filepath)
            tries = 0
        except HTTPError as e:
            if e.code == 504 and tries > 0:
                tries -= 1
            else:
                raise


def _normalize_uri(uri):
    import urllib

    scheme, rest = urllib.parse.splittype(uri)
    rest = urllib.parse.quote(rest)
    return scheme + ":" + rest
