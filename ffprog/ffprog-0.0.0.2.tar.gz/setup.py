#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import io
import os
import re

from setuptools import find_packages, setup

DEPENDENCIES = ['aiofiles>=0.4.0']
EXCLUDE_FROM_PACKAGES = ["contrib", "docs", "tests*"]
CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()


def get_version():
    main_file = os.path.join(CURDIR, "ffprog", "main.py")
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(main_file, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setup(
    name="ffprog",
    version=get_version(),
    author="Vitalii Honchar",
    author_email="honchar.vitalii@gmail.com",
    description="FFmpeg progress info package",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/Illicitus/ffprog",
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/Illicitus/ffprog/issues',
        'Source': 'https://github.com/Illicitus/ffprog',
    },
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    keywords=['FFMPEG', 'FFPROBE', 'FFPROG'],
    scripts=[],
    entry_points={"console_scripts": ["ffprog=ffprog.main:main"]},
    zip_safe=False,
    install_requires=DEPENDENCIES,
    extras_require={
        'dev': ['isort'],
        'test': ['green', 'coverage'],
    },
    test_suite="tests.test_project",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
