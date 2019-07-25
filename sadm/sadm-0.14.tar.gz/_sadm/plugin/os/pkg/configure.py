# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm import dist

__all__ = ['cfgfilter', 'configure']

_options = ('update', 'install', 'remove', 'prune')

def cfgfilter(opt):
	dn = dist.getname() + '.'
	if opt.startswith(dn):
		for n in _options:
			n = n + '.'
			if opt.endswith(n):
				return opt
	return None

def configure(env, cfg):
	env.settings.merge(cfg, 'os.pkg', _options)
