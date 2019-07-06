from os import path

from setuptools import setup

from HitBTCMonster import (
    __name__, __version__, __license__, __description__, __repository__, __author__
)

PATH = path.abspath(path.dirname(__file__))
with open(path.join(PATH, 'README.rst'), encoding='utf-8') as README:
    long_description = README.read()

setup(
    name=__name__,
    url=__repository__,
    version=__version__,
    license=__license__,
    description=__description__,
    long_description=long_description,
    author=__author__,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=[__name__, '%s.api' % __name__, '%s.wss' % __name__],
    keywords=['HitBTC', 'WSS', 'API'],
    install_requires=['websocket-client', 'requests'],
    project_urls={
        'Source': '%s.git' % __repository__
    },
)
