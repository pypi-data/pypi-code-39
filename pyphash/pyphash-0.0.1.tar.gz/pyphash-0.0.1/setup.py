#!/usr/bin/env python

# pyphash - extremely simple wrapper around crypt(3).
# Copyright 2019 Zack Weinberg <zackw@panix.com>.
# Distributed under the terms of the Apache Software License, version 2.0;
# see the file LICENSE in the source distribution for details.

import os
import sys

from setuptools import setup, Extension

SRCDIR = os.path.abspath(os.path.dirname(__file__))

# Read a file within the source tree that may or may not exist, and
# decode its contents as UTF-8, regardless of external locale settings.
def read_file(filename):
    filepath = os.path.join(SRCDIR, filename)
    try:
        raw = open(filepath, "rb").read()
    except (IOError, OSError):
        return ""
    return raw.decode("utf-8")


# Discard unwanted top matter from README.md for reuse as the long
# description.  Specifically, we discard everything up to and
# including the first Markdown header line (begins with a '#') and
# any blank lines immediately after that header.
def read_and_trim_readme():
    readme = read_file("README.md").splitlines()
    found_first_header = False
    start = None
    for i, line in enumerate(readme):
        # Both leading and trailing horizontal whitespace may be
        # significant in Markdown, so we don't strip any.
        if found_first_header:
            if line:
                # This is the first non-blank line after the
                # first header, and therefore the first line
                # we want to preserve.
                start = i
                break
        elif line and line[0] == '#':
            found_first_header = True
    else:
        sys.stderr.write("Failed to parse README.md\n")
        sys.exit(1)

    return "\n".join(readme[start:])

setup(
    name = "pyphash",
    version = "0.0.1",
    description = "extremely simple wrapper around crypt(3)",
    long_description = read_and_trim_readme(),
    long_description_content_type = "text/markdown",
    maintainer = "Zack Weinberg",
    maintainer_email = "zackw@panix.com",
    url = "https://github.com/zackw/pyphash",
    license = "Apache",
    ext_modules = [
        Extension("pyphash", ["pyphash.c"],
                  libraries = ["crypt"]
        )
    ],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: Apache Software License",
    ]
)
