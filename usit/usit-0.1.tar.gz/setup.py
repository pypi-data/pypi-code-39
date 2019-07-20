# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 17:30:03 2019

@author: qchat
"""

from distutils.core import setup

#with open('README.md') as f:
#    long_description = f.read()
    

setup(
    name = 'usit',
    packages = ['usit'],
    data_files = [('usit', ['config/*'])],
    version = '0.1',  # Ideally should be same as your GitHub release tag varsion
    description = 'Universal Scanning Interface : Python automation package for scientific laboratory experiments',
#    long_description = long_description,
#    long_description_content_type='text/markdown',
    author = 'Quentin Chateiller',
    author_email = 'q.chateiller@gmail.com',
    url = 'https://upload.pypi.org/legacy/',
    download_url = 'https://github.com/qcha41/usit/archive/0.1.tar.gz',
    keywords = ['Universal','Scanning','Interface','automation','scientific','laboratory','experiments','measures']
)

