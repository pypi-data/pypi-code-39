#!/usr/bin/env python3

from setuptools import setup

setup(
	name="pyvn",
	version='1.4',
	license='MIT',
	description='Python3 Ivnosys Utils',
	author='Ivnosys Soluciones S.L.',
	author_email='jbiosca@ivnosys.com',
	url='https://ivnosys.com/',
	python_requires='>=3.5',
	#packages=["lib"],
	packages=["pyvn"],
	package_dir={"pyvn": "src"},
	#py_modules=['ivscript', 'jdata', 'josen', 'run']
	keywords = ['utils'],
	install_requires=[
		'setuptools',
		'dicttoxml',
		'xmltodict',
		'ruamel.yaml',
		'colorama',
		'setproctitle',
	],
	classifiers=[
		# 5 - Production/Stable
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'License :: OSI Approved :: MIT License',
	],

)
