# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

def test_os(testing_plugin):
	p = testing_plugin('os')
	assert p.configure()
