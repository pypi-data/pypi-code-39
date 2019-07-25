"""Setuptools entry point."""
import codecs
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

dirname = os.path.dirname(__file__)

long_description = (
    codecs.open(os.path.join(dirname, 'README.rst'), encoding='utf-8').read() + '\n' +
    codecs.open(os.path.join(dirname, 'CHANGES.rst'), encoding='utf-8').read()
)

setup(
    name='ddd-base',
    version='0.0.2',
    description='DDD base framework for python',
    long_description=long_description,
    author='Sun Wei',
    author_email='wayde.sun@gmail.com',
    url='https://github.com/sunwei/ddd-base',
    packages=['ddd_base'],
    install_requires=[],
    classifiers=CLASSIFIERS)
