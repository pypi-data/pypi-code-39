# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name='ruamel.browser.client',
    version_info=(0, 2, 10),
    __version__='0.2.10',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='zmq based client to talk with ruamel.browser.server',
    license='MIT License',
    since=2019,
    entry_points='rbc=ruamel.browser.client.__main__:main',
    install_requires=['ruamel.appconfig', 'ruamel.std.argparse>=0.8', 'pyzmq'],
    classifiers=[
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: Implementation :: CPython',
            'Topic :: Internet :: WWW/HTTP',
    ],
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']

from .client import Client  # NOQA
