#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

# compiler = "mingw32"

# system_name = platform.system().lower()
# is_windows = system_name == 'windows'
# file_dir = os.path.abspath(os.path.dirname(__file__))

setup(
    name='tracking_util',
    version='0.1.rc4',
    description='Util scripts for tracking tasks',
    author='tianling.bian',
    author_email='bian_tianling@sjtu.edu.cn',
    packages=['tracking_util/io', 'tracking_util/utils'],
    install_requires=['matplotlib', 'opencv-python', 'tqdm', 'numpy', 'scipy'],
    # entry_points={
    #     'console_scripts': [
    #         'find_max=tools.eval.find_max:main',
    #         'e2e_eval=tools.eval.e2e_eval:main'
    #     ],
    # },
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    long_description=open('README.md').read())
