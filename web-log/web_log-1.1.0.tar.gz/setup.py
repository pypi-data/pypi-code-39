#!/usr/bin/env python

from setuptools import setup

setup(
    name="web_log",
    version="1.1.0",
    packages=["web_log"],
    author="Software Innovation, Equinor ASA",
    author_email="fg_gpl@equinor.com",
    url="https://github.com/equinor/weblog",
    license="MIT",
    description="Logs json logs to somewhere",
    entry_points={"console_scripts": ["wlog=web_log:wlog"]},
    install_requires=["requests"],
)
