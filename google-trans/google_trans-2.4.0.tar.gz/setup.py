#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import re
import sys

from setuptools import setup, find_packages


def get_file(*paths):
    path = os.path.join(*paths)
    try:
        with open(path, 'rb') as f:
            return f.read().decode('utf8')
    except IOError:
        pass


def get_version():
    init_py = get_file(os.path.dirname(__file__), 'google_trans', '__init__.py')
    pattern = r"{0}\W*=\W*'([^']+)'".format('__version__')
    version, = re.findall(pattern, init_py)
    return version


def get_description():
    init_py = get_file(os.path.dirname(__file__), 'google_trans', '__init__.py')
    pattern = r'"""(.*?)"""'
    description, = re.findall(pattern, init_py, re.DOTALL)
    return description


def get_readme():
    return get_file(os.path.dirname(__file__), 'README.rst')


def install():
    setup(
        name='google_trans',
        version=get_version(),
        description=get_description(),
        long_description="google translation for python",
        long_description_content_type="text/markdown",
        license='MIT',
        author='scoefield',
        author_email='scoefielddeng' '@' 'gmail.com',
        url='https://github.com/Scoefield/GoogleTransLibrary',
        classifiers=['Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Education',
                     'Intended Audience :: End Users/Desktop',
                     'License :: Freeware',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Education',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'Programming Language :: Python :: 3.6'],
        packages=find_packages(exclude=['docs']),
        keywords='google translate translator',
    )


if __name__ == "__main__":
    install()
