#!/usr/bin/env python

from distutils.core import setup, Command
import os
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

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
    version='1.0.3',
    description='Video Converter library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/jamieoglindsey0/python-video-converter/-/archive/1.0.3/python-video-converter-1.0.3.tar.gz',
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
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
