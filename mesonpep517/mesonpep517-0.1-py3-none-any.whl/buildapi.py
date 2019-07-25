"""PEP-517 compliant buildsystem API"""
import contextlib
import tempfile
import tarfile
import logging
import os
import json
import shutil
import subprocess
import sys

from gzip import GzipFile
from pathlib import Path
from datetime import datetime
from collections import namedtuple
from wheel.wheelfile import WheelFile

__version__ = '0.1'

# PEP 517 specifies that the CWD will always be the source tree
pyproj_toml = Path('pyproject.toml')

def meson(*args, config_settings=None):
    try:
        return subprocess.check_output(['meson'] + list(args))
    except Exception as e:
        print('----------------------------------------------------', file=sys.stderr)
        print(args, file=sys.stderr)
        print('----------------------------------------------------', file=sys.stderr)
        import ipdb; ipdb.set_trace()
        raise e

def meson_introspect(_dir, introspect_type):
    return json.loads(meson('introspect', _dir, '--' + introspect_type))


@contextlib.contextmanager
def cd(path):
    CWD = os.getcwd()

    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(CWD)

def get_requires_for_build_wheel(config_settings=None):
    """Returns a list of requirements for building, as strings"""
    return ['setuptools']

# For now, we require all dependencies to build either a wheel or an sdist.
get_requires_for_build_sdist = get_requires_for_build_wheel


wheel_file_template = """\
Wheel-Version: 1.0
Generator: backend {version}
Root-Is-Purelib: true
""".format(version=__version__)


def _write_wheel_file(f, *, supports_py2=False):
    f.write(wheel_file_template)
    if supports_py2:
        f.write("Tag: py2-none-any\n")
    f.write("Tag: py3-none-any\n")


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None, builddir=None):
    """Creates {metadata_directory}/foo-1.2.dist-info"""
    if not builddir:
        builddir = tempfile.TemporaryDirectory().name
        meson(builddir, config_settings=config_settings)
    project = meson_introspect(builddir, 'projectinfo')

    dist_info = Path(metadata_directory, '{}-{}.dist-info'.format(
        project['descriptive_name'], project['version']))
    dist_info.mkdir()

    with (dist_info / 'WHEEL').open('w') as f:
        _write_wheel_file(f, supports_py2=False)

    print(dist_info / 'METADATA')
    with (dist_info / 'METADATA').open('w') as f:
        fields = {
            'Metadata-Version': '2.1',
            'Name': project['descriptive_name'],
            'Version': project['version'],
            'Summary': None,
            'Home-page': None,
            'License': None,
        }

        for field, value in fields.items():
            if value is None:
                value = project.get(field.lower(), None)

            if value is not None:
                f.write("{}: {}\n".format(field, value))

    return dist_info.name

class WheelBuilder:
    def __init__(self):
        self.wheel_zip = None
        self.builddir = tempfile.TemporaryDirectory()
        self.installdir = tempfile.TemporaryDirectory()

    def build(self, wheel_directory, config_settings, metadata_dir):
        meson(self.builddir.name, '--prefix', self.installdir.name, config_settings=config_settings)

        if not metadata_dir:
            metadata_dir = prepare_metadata_for_build_wheel(wheel_directory, builddir=self.builddir.name)
        project = meson_introspect(self.builddir.name, 'projectinfo')
        target_fp = wheel_directory / '{}-{}-py3-none-any.whl'.format(
            project['descriptive_name'],
            project['version'],
        )
        self.wheel_zip = WheelFile(target_fp, 'w')
        for f in os.listdir(os.path.join(wheel_directory, metadata_dir)):
            self.wheel_zip.write(os.path.join(wheel_directory, metadata_dir, f),
                arcname=os.path.join(metadata_dir, f))
        print("Adding %s" % os.path.join(wheel_directory, metadata_dir), file=sys.stderr, flush=True)

        # Make sure everything is built
        subprocess.check_call(['ninja', '-C', self.builddir.name, 'install'])
        for sfile, installpath in meson_introspect(self.builddir.name, 'installed').items():
            if "site-packages" in installpath:
                while os.path.basename(installpath) != 'site-packages':
                    installpath = os.path.dirname(installpath)
                self.wheel_zip.write_files(installpath)
                break
        self.wheel_zip.close()
        return str(target_fp)

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    """Builds a wheel, places it in wheel_directory"""
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', file=sys.stderr)
    print(wheel_directory, file=sys.stderr)
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', file=sys.stderr)
    return WheelBuilder().build(Path(wheel_directory), config_settings, metadata_directory)


PKG_INFO = """\
Metadata-Version: 1.1
Name: {name}
Version: {version}
Summary: {summary}
Home-page: {home_page}
Author: {author}
Author-email: {author_email}
"""

def build_sdist(sdist_directory, config_settings=None):
    """Builds an sdist, places it in sdist_directory"""
    distdir = Path(sdist_directory)
    with tempfile.TemporaryDirectory() as builddir:
        with tempfile.TemporaryDirectory() as installdir:
            meson(builddir, '--prefix', installdir, config_settings=config_settings)
            subprocess.check_call(['ninja', '-C', builddir, 'dist'])

            project = meson_introspect(builddir, 'projectinfo')

            tf_dir = '{}-{}'.format(project['descriptive_name'], project['version'])
            distfilename = '%s.tar.xz' % tf_dir
            mesondisttar = tarfile.open(Path(builddir) / 'meson-dist' / distfilename)
            mesondisttar.extractall(installdir)

            pkg_info = PKG_INFO.format(
                name=project['descriptive_name'],
                version=project['version'],
                summary="Unknown",
                home_page="Unknown",
                author="Unknown",
                author_email="Unknown",
            )

            target = distdir / distfilename
            source_date_epoch = os.environ.get('SOURCE_DATE_EPOCH', '')
            mtime = int(source_date_epoch) if source_date_epoch else None
            with GzipFile(str(target), mode='wb', mtime=mtime) as gz:
                with cd(installdir):
                    with tarfile.TarFile(str(target), mode='w', fileobj=gz, format=tarfile.PAX_FORMAT) as tf:
                        tf.add(tf_dir, recursive=True)
                        with open(Path(installdir) / tf_dir / 'PKG-INFO', mode='w') as fpkginfo:
                            fpkginfo.write(pkg_info)
                            fpkginfo.flush()
                            tf.add(Path(tf_dir) / 'PKG-INFO')
    return target.name
