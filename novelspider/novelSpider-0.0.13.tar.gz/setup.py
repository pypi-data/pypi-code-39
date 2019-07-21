#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages
from novelSpider.task import Task

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='novelSpider',
    version=Task.__version__,
    url='https://github.com/gugutianle/novelSpider',
    license='MIT License',
    author='gugutianle',
    install_requires=[ 'beautifulsoup4==4.6.3', 'Cython>=0.29.7', 'lxml==4.3.0', 'requests==2.20.1', 'mysqlclient==1.3.7', 'SQLAlchemy==1.3.1'],
    author_email='gugutianle@ggo.la',
    description='采集中文小说网站的爬虫',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ]
)
