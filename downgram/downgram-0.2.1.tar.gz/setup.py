# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import re
from setuptools import setup

with open("README.md", "rb") as rd:
    long_desc = rd.read().decode("utf-8")

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('downgram/downgram.py').read(),
    re.M
    ).group(1)

setup(
    name='downgram',
    version=version,
    packages=['downgram'],
    entry_points= {
        "console_scripts": ['downgram = downgram.downgram:main']
    },
    author='josopu',
    author_email='piperinoxi@gmail.com',
    description='DownGram can download media from Telegram, using Telethon.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url='https://github.com/josopu/DownGram',
    data_failes=[('config',['downgram/settings.ini'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: GNU General Public License v3 or later (GPLv3+)",
    ],
)
