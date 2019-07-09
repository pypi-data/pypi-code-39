# SnapLogic - Data Integration
#
# Copyright (C) 2018, SnapLogic, Inc.  All rights reserved.
#
# This program is licensed under the terms of
# the SnapLogic Commercial Subscription agreement.
#
# 'SnapLogic' is a trademark of SnapLogic, Inc.

import setuptools

with open("README.md", "r") as readme_file:
    LONG_DESC = readme_file.read()

setuptools.setup(
    name="snaplogic",
    version="0.0.3",
    author="Jump Thanawut",
    author_email="jumpthanawut@snaplogic.com",
    description="This package contains modules to be used with SnapLogic.",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    url="https://www.snaplogic.com",
    packages=setuptools.find_packages(),
    install_requires=[
        "clipboard==0.0.4",
        "jsonpickle==1.0",
        "numpy==1.15.3",
        "pycrypto==2.6.1",
        "python-dateutil==2.7.5",
        "pytz==2018.7",
        "pandas==0.23.4",
        "requests==2.20.0",
        "jupyter==1.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)