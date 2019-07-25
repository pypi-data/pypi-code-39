#!/usr/bin/env python
#-*- coding:utf-8 -*-



from setuptools import setup, find_packages

setup(
    name = "openimu_update",
    version = "0.0.3",
    keywords = ("pip","python-openimu","openimu package"),
    description = "openimu package",
    long_description = "easy install the openimu essential package",
    license = "aceinna Licence test",

    url = "https://github.com/Aceinna/python-openimu",
    author = "Yifan",
    author_email = "yifanff@126.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy"]
)
