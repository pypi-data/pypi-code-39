#!/usr/bin/env python

import os
import sys
from setuptools import setup, Extension
from subprocess import check_call
from distutils import log
from distutils.spawn import find_executable
from distutils.command.build_ext import build_ext as BuildCommand

import sipconfig


class CustomBuild(BuildCommand):
    user_options = [
        ('qmake=', None, "qmake to use"),
        ('sip=', None, "sip to use"),
        ('sip-incdir=', None, 'sip include directory (.sip)'),
        ('pyqt-sipdir=', None, 'sip include directory (.sip) for PyQt5'),
    ] + BuildCommand.user_options

    def _run_command(self, cmd, env=None):
        log.debug(' '.join(cmd))
        try:
            return check_call(cmd, env=env)
        except:
            log.error('command failed [%s]' % (' '.join(cmd)))
            raise

    def initialize_options(self):
        BuildCommand.initialize_options(self)
        self.qmake = find_executable('qmake')
        self.sip = find_executable('sip')
        sconf = sipconfig.Configuration()
        self.sip_incdir = sconf.default_sip_dir
        self.pyqt_sipdir = os.path.join(self.sip_incdir, 'PyQt5')

    def run(self):
        ext = self.extensions[0]
        self._run_command([
            'python', 'configure.py', '--verbose',
            '--qmake', self.qmake,
            '--sip-incdir', self.sip_incdir,
            '--sip', self.sip,
            '--pyqt-sipdir', self.pyqt_sipdir,
            '--no-sip-files',
            '--destdir', os.path.join(self.get_ext_fullpath(ext.name), ".."),
        ])
        self._run_command(['qmake'])
        if sys.platform == "win32":
            self._run_command(['nmake', 'install'])
        else:
            self._run_command(['make', 'install'])


class CustomExt(Extension):
    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        Extension.__init__(self, name, sources=[])


def _generate_python():
    if not os.path.exists('customeventfilters'):
        try:
            os.mkdir('customeventfilters')
        except (IOError, OSError):
            pass
    with open(os.path.join('customeventfilters', '__init__.py'), "w+") as f:
        f.write("from __future__ import absolute_import\n")
        f.write("from .customeventfilters import *\n")


_generate_python()

setup(
    name='customeventfilters',
    version='0.6.2',
    description='clarilab custom event filters',
    long_description=('Custom PyQt5 event filters'),
    maintainer='Laurent Coustet',
    maintainer_email='laurent.coustet@clarisys.fr',
    license='BSD',
    packages=['customeventfilters'],
    ext_modules=[CustomExt('customeventfilters.customeventfilters')],
    cmdclass = {
        'build_ext': CustomBuild,
    }
)
