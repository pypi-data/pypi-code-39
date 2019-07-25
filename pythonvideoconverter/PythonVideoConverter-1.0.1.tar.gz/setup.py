#!/usr/bin/env python

from distutils.core import setup, Command
import os


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        self._testdir = os.path.join(os.getcwd(), 'test')

    def finalize_options(self):
        pass

    def run(self):
        os.chdir(self._testdir)
        retval = os.system('python3.7 -m test')
        if retval != 0:
            raise Exception('tests failed')


class DocCommand(Command):
    user_options = []

    def initialize_options(self):
        self._docdir = os.path.join(os.getcwd(), 'doc')

    def finalize_options(self):
        pass

    def run(self):
        os.chdir(self._docdir)
        os.system('make html')


setup(
    name='PythonVideoConverter',
    version='1.0.1',
    description='Video Converter library',
    url='https://gitlab.com/jamieoglindsey0/python-video-converter',

    author='Jamie Lindsey',
    author_email='admin@materialwebdesign.online',

    cmdclass={
        'test': TestCommand,
        'doc': DocCommand
    },

    packages=[
        'converter',
        'converter.codecs',
    ],

    setup_requires=[
        'six',
    ],
)
