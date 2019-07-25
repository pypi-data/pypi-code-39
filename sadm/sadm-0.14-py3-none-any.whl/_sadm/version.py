# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

try:
	from _sadm._version import version as _version # pragma: no cover
except ImportError:
	_version = 'master'

try:
	from _sadm._version import version_build as _version_build # pragma: no cover
except ImportError:
	_version_build = None

__all__ = ['get', 'string']

def get():
	return _version

def build():
	if _version_build is None:
		return 'devel'
	return _version_build

def string():
	s = get()
	if _version_build is not None:
		s = "%s (build %s)" % (s, build())
	return '%(prog)s version ' + s
