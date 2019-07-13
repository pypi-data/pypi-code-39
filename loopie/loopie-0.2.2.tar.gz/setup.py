'''
Created on Saturday 13/07/2019

@author: yaztown
'''

from setuptools import setup

import os

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
		name='loopie',
		packages=['loopie',
                  'loopie.core',
                  'loopie.core.base_threads',
                  'loopie.core.datetime',
                  'loopie.core.json',
                  'loopie.core.metaclasses',
                  'loopie.logging',
                  'loopie.net',
        ],
		version='0.2.2',
		license="GPLv3",
		description='A simple python framework for creating a looping application (Service).',
		long_description=README,
		long_description_content_type="text/markdown",
# 		python_requires='~=3.6',
		author='Yaztown',
		author_email='yaztown@gmail.com',
		url='https://github.com/yaztown/loopie',
		download_url='https://github.com/yaztown/loopie/archive/v0.2.2.tar.gz',
		keywords=['loopie', 'loop', 'looping', 'mainloop', 'thread', 'threading', 'Pi', 'Raspberry Pi', 'RPi'],
		install_requires=[
	        'flask',
	        'flask_cors',
	        'flask_jsonrpc',
	        'wsgiserver',
	        'pytz',
      	],
		classifiers=[
		    'Development Status :: 5 - Production/Stable',
		    'Intended Audience :: Developers',
		    'Topic :: Software Development :: Build Tools',
		    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		    'Programming Language :: Python :: 3',
		    'Programming Language :: Python :: 3.4',
		    'Programming Language :: Python :: 3.5',
		    'Programming Language :: Python :: 3.6',
		    'Programming Language :: Python :: 3.7',
		 ],
)
