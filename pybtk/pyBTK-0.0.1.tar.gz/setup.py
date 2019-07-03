# -*- coding: utf-8 -*-
from setuptools import setup,find_packages

#------------------------- INSTALL--------------------------------------------
setup(name = 'pyBTK',
    version = "0.0.1",
    author = 'Fabien Leboeuf',
    author_email = 'fabien.leboeuf@gmail.com',
    description = "python3 wrapping of the Biomechanical toolkit",
    keywords = 'c3d, mocap',
    packages=find_packages(),
	include_package_data=True,
    license='BSD License',
    classifiers=['Programming Language :: Python',
                 'Operating System :: Microsoft :: Windows',
                 'Natural Language :: English'],
    )
