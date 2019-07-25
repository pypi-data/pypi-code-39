# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm import dist
from _sadm.configure import pluginsList, getPlugin

dist._name = 'testing'

def test_testing_plugin(testing_plugin):
	p = testing_plugin('testing', ns = '_sadmtest')
	assert p.configure()

def test_all_configure(testing_plugin):
	for n in pluginsList():
		if n in ('testing', 'sadm', 'sadmenv'):
			continue
		p = testing_plugin(n)
		assert p.configure(), "%s plugin.configure failed" % n
