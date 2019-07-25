#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

# https://packaging.python.org/guides/distributing-packages-using-setuptools/

from datetime import datetime
from os import makedirs, path, unlink
from setuptools import setup, find_packages
from sys import argv

def _build():
	if not path.isfile('./build/.gitignore'):
		makedirs('./build', exist_ok = True)
		with open('./build/.gitignore', 'w') as fh:
			fh.write('*\n')

def _clean():
	if path.isfile('./build/.gitignore'):
		unlink('./build/.gitignore')

def _buildInfo():
	if path.isfile('./_sadm/_version.py'):
		now = datetime.utcnow()
		with open('./_sadm/_version.py', 'a') as fh:
			fh.write("version_build = '%s'\n" % now.strftime('%y%m%d.%H%M%S'))

def main():

	try:
		cmd = argv[1]
	except IndexError:
		cmd = 'none'

	if cmd in ['build', 'dist', 'install']:
		_build()
	elif cmd == 'clean':
		_clean()

	with open('requirements.txt', 'r') as fh:
		deps = fh.read().splitlines()

	setup(
		author = 'Jeremías Casteglione',
		author_email = 'jrmsdev@gmail.com',
		python_requires = '~=3.4',
		setup_requires = ['wheel>=0.33', 'setuptools_scm>=3.3'],
		install_requires = deps,
		use_scm_version = {'write_to': '_sadm/_version.py'},
		py_modules = ['sadm'],
		packages = find_packages(),
		include_package_data = True,
	)

	_buildInfo()

if __name__ == '__main__':
	main()
