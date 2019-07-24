"""
Copyright (C) 2019 Kunal Mehta <legoktm@member.fsf.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from setuptools import setup

setup(
    name='free-torrents',
    version='1.0.0',
    packages=['free_torrents'],
    url='https://legoktm.com/w/index.php?title=free-torrents',
    license='GPL-3.0-or-later',
    author='Kunal Mehta',
    author_email='legoktm@member.fsf.org',
    description='Script to facilitate downloading '
                'free (as-in-speech) torrents',
    install_requires=[
        'requests'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'free-torrents = free_torrents:main'
        ]
    }
)
