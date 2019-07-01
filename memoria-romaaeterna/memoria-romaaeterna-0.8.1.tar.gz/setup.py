#!/usr/bin/env python3
#
# This file is part of Memoria.
#
# Copyright (C) 2019 - Thomas Dähnrich <develop@tdaehnrich.de>
#
# Memoria is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# Memoria is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Memoria. If not, see <http://www.gnu.org/licenses/>.

import os
import subprocess

from glob import glob
from memoria.settings import VERSION
from setuptools import setup


# create locale files

languages = ('de', 'en_GB')

for lang in languages:
    locale_dir = os.path.join('locale', lang, 'LC_MESSAGES')
    locale_file = os.path.join(locale_dir, 'memoria.mo')
    po_file = os.path.join('po', lang + '.po')
    if not os.path.exists(locale_dir):
        os.makedirs(locale_dir)
        subprocess.call(['msgfmt', '-o', locale_file, po_file])


# create desktop file

template_file = os.path.join('data', 'com.gitlab.RomaAeterna.Memoria.desktop.in')
desktop_file = os.path.join('data', 'com.gitlab.RomaAeterna.Memoria.desktop')

if not os.path.exists(desktop_file):
    subprocess.call(['msgfmt', '--desktop', '--template={}'.format(template_file),
        '--output-file={}'.format(desktop_file), '-d', 'po'])


# get README description

with open('README.rst', 'r') as f:
    long_description = f.read()


# install application

setup(
    name = 'memoria-romaaeterna',
    version = VERSION,
    license = 'GPL-3+',
    packages = [
        'memoria',
        'memoria.simpleaudio',
    ],
    package_data = {
        'memoria.simpleaudio': ['LICENSE.txt', 'README.rst', '_simpleaudio.so'],
    },
    scripts = ['bin/memoria'],
    data_files = [
        ('share/applications', [desktop_file]),
        ('share/icons/hicolor/16x16/apps', glob('data/icons/hicolor/16x16/apps/*')),
        ('share/icons/hicolor/22x22/apps', glob('data/icons/hicolor/22x22/apps/*')),
        ('share/icons/hicolor/24x24/apps', glob('data/icons/hicolor/24x24/apps/*')),
        ('share/icons/hicolor/32x32/apps', glob('data/icons/hicolor/32x32/apps/*')),
        ('share/icons/hicolor/48x48/apps', glob('data/icons/hicolor/48x48/apps/*')),
        ('share/icons/hicolor/256x256/apps', glob('data/icons/hicolor/256x256/apps/*')),
        ('share/icons/hicolor/512x512/apps', glob('data/icons/hicolor/512x512/apps/*')),
        ('share/locale/de/LC_MESSAGES', ['locale/de/LC_MESSAGES/memoria.mo']),
        ('share/locale/en_GB/LC_MESSAGES', ['locale/en_GB/LC_MESSAGES/memoria.mo']),
        ('share/memoria/pixmaps', glob('data/pixmaps/*')),
        ('share/memoria/sounds', glob('data/sounds/*')),
        ('share/memoria/ui', glob('data/ui/*')),
    ],
    python_requires = '>=3.3',
    author = 'Thomas Dähnrich',
    description = 'Play Memory (Matching) for up to four players',
    long_description = long_description,
    keywords = ['education', 'game'],
    url = 'https://gitlab.com/romaaeterna/memoria',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Desktop Environment :: Gnome',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
    ],
)
