# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['traitlet_widgets']
install_requires = \
['ipywidgets>=7.5,<8.0', 'traitlets>=4.3,<5.0']

setup_kwargs = {
    'name': 'traitlet-widgets',
    'version': '0.1.2',
    'description': 'A library which provides the ability to create widget views for traitlet `HasTraits` models, and also to observe changes in a model',
    'long_description': None,
    'author': 'Angus Hollands',
    'author_email': 'goosey15@gmail.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
