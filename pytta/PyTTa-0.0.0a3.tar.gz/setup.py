# -*- coding: utf-8 -*-
"""
PyTTa setup file
=================

@Autor:
- João Vitor Gutkoski Paes, joao.paes@eac.ufsm.br

"""

#%%
from setuptools import setup

settings = {
    'name': 'PyTTa',
    'version': '0.0.0a3',
    'description': 'Signal processing tools for acoustics and vibrations in python.',
    'url': 'http://github.com/PyTTAmaster/PyTTa/tree/v0.0.0a2',
    'author': 'Marcos Reis, Matheus Lazarin, João Vitor Paes',
    'packages': ['pytta'],
    'author_email': 'joao.paes@eac.ufsm.br',
    'license': 'MIT',
    'install_requires': ['numpy','scipy', 'matplotlib','sounddevice'],
}
setup(**settings)
