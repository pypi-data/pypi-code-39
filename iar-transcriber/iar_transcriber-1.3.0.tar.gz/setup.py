#!python3
# coding:utf8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="iar_transcriber",
                 version="1.3.0",
                 author="Iván Arias Rodríguez",
                 author_email="ivan.arias.rodriguez@gmail.com",
                 description="A phonetic transcriber for Spanish language.",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/ivansiiito/iar_transcriber",
                 packages=setuptools.find_packages(),
                 classifiers=["Programming Language :: Python :: 3",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent",
                              ],
                 install_requires=['nltk', 'num2words', 'roman', 'python-dateutil', 'iar_tokenizer'],
                 )
