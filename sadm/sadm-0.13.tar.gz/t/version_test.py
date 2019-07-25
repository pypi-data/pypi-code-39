# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm import version

def test_get_build():
	v = version.get()
	assert isinstance(v, str)
	assert v == 'master'
	b = version.build()
	assert isinstance(b, str)
	assert b == 'devel'

def test_string():
	v = version.string()
	assert isinstance(v, str)
	assert v == '%(prog)s version master (build devel)'
