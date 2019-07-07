#!/usr/bin/env python
# coding: utf-8

from setuptools import setup,find_packages

setup(
    name='skaida',
    version='1.1.5',
    author='Shu Kougetsu',
    author_email='zefuirusu@qq.com',
    url='https://user.qzone.qq.com/2078766287/infocenter',
    description=u"The name comes from AIDA in Marvel's Agents of SHIELD, short for Artificial Intelligence Digital Assistant.",
    packages = find_packages(),
    install_requires=['numpy>=1.16.2','pandas>=0.24.2','python-docx>=0.8.10','xlrd>=1.2.0','xlwt>=1.3.0','openpyxl>=2.6.1','selenium>=3.141.0'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            #'catatest=skaida:catatest',
            #'samprepare=skaida:samprepare',
            #'projpp=skaida:projpp',
            #'simplegoo=skaida:simplegoo',
            #'opsite=skaida:opsite',
            #'findfile=skaida:findfile'
            
        
        ]
    }
)
