# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

long_description = """Collection of tools to perform experiments."""

setup(
    name='Experimentor',
    version='0.0.1',
    description='Experiments performed with Python',
    packages=find_packages(),
    url='https://github.com/aquilesC/experimentor',
    license='GPLv3',
    author='Aquiles Carattino',
    author_email='aquiles@uetke.com',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    include_package_data=True,
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
)

