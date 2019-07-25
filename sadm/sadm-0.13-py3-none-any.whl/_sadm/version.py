# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

try:
	from _sadm._version import version as _version
	from _sadm._version import version_build as _version_build # pragma: no cover
except ImportError:
	_version = 'master'
	_version_build = 'devel'

__all__ = ['get', 'string']

def get():
	return _version

def build():
	return _version_build

def string():
	s = "%s (build %s)" % (get(), build())
	return '%(prog)s version ' + s
