#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='skoffice',
    version='1.0.0',
    author='Shu Kougetsu',
    author_email='zefuirusu@qq.com',
    url='https://user.qzone.qq.com/2078766287/infocenter',
    description=u'Assistant Tool for MS Office',
    packages=['skoffice'],
    install_requires=['numpy>=1.16.2','pandas>=0.24.2','python-docx>=0.8.10','xlrd>=1.2.0','xlwt>=1.3.0','openpyxl>=2.6.1','selenium>=3.141.0'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            #'catatest=skoffice:catatest',
            #'samprepare=skoffice:samprepare',
            
        ]
    }
)
