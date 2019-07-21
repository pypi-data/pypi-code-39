###########################################################################
# Helios is Copyright (C) 2016-2018 Kyle Robbertze
# <paddatrapper@debian.org>
#
# Helios is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Helios is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Helios.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################
from codecs import open
from setuptools import setup, find_packages

setup(
    name='helios-monitor',
    version='1.0.0',
    description='Monitors the audio levels of a stream',
    long_description='Helios monitors the audio levels of a stream over time.',
    url='https://salsa.debian.org/debconf-video-team/helios',
    author='Kyle Robbertze',
    author_email='paddatrapper@debian.org',
    license='GPL-3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Other Audience',
        'Topic :: Multimedia :: Sound/Audio',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='streaming audio monitor R128',
    packages=find_packages(),
    install_requires=['influxdb'],
    package_data={
        '': ['LICENCE.md', 'helios.ini.example'],
    },
    entry_points={
        'console_scripts': ['helios=helios:run'],
    },
)
