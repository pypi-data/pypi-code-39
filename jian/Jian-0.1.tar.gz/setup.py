# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2019/07/01 <https://7yue.in>
"""
from __future__ import print_function
from setuptools import setup

setup(
    name="Jian",
    version="0.1",
    author="Jarrott Xu",
    author_email="xqiqio7@gmail.com",
    description="Jarrott Flask中实现高可用的扩展",
    license="Apache License",
    url="",
    packages=['jian'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)