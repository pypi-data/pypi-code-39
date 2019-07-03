#!/usr/bin/env python
# -*-coding:utf-8-*-
from setuptools import setup, find_packages

setup(
    name='http-api-sdk',
    version='2.3.0',
    description=
    '扩展你的QQ/微信机器人用途，提供跨框架平台的PHP/Java/Python/NodeJS等编程语言SDK。https://github.com/ksust/HTTP--API',
    long_description=open('README.rst', encoding='utf-8').read(),
    author='ksust',
    author_email='admin@ksust.com',
    maintainer='ksust',
    maintainer_email='admin@ksust.com',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/ksust/HTTP--API',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'requests>=2.14.2',
    ]
)
