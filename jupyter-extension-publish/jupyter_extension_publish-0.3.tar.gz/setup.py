#!/usr/bin/env python

import setuptools
from distutils.core import setup

setup(
        name='jupyter_extension_publish',
        version='0.3',
        description='jupyter extension for publish notebook',
        author='Keunhui Park',
        author_email='keunhui.park@gmail.com',
        packages=['jupyter_extension_publish'],
        include_package_data=True,
        install_requires=[
            'ipython >= 4',
            'notebook >= 4.3.1',
            'jupyter',
            'boto3',
            ],
        )
