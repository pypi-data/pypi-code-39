# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:34:37 2019

@author: wangyunxiang
"""

import setuptools

with open("README.md","r") as f:
    long_description = f.read()
    
setuptools.setup(
        name="redtongue",
        version="0.0.1",
        author="redtongue",
        description="niu bi redtongue!!!!",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/redtongue",
        packages=setuptools.find_namespace_packages(),
        classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
        ],
)