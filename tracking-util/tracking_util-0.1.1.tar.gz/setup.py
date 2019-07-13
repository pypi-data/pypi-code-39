#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# compiler = "mingw32"

# system_name = platform.system().lower()
# is_windows = system_name == 'windows'
# file_dir = os.path.abspath(os.path.dirname(__file__))

setup(
    name='tracking_util',
    version='0.1.1',
    description='Util scripts for tracking tasks',
    author='tianling.bian',
    author_email='bian_tianling@sjtu.edu.cn',
    packages=find_packages(),
    install_requires=['matplotlib', 'opencv-python', 'tqdm', 'numpy', 'scipy'],
    zip_safe=False,
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
