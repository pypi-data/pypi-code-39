
import chainer.functions as F

from .gmm_layer import GMMLayer

class FVLayer(GMMLayer):

	def encode(self, x):
		gamma = self.soft_assignment(x)
		_x, *params = self._expand_params(x)

		_gamma = self.xp.expand_dims(gamma.array, axis=2)
		_mu, _sig, _w = [p.array for p in params]

		_x_mu_sig = (_x - _mu) / _sig

		G_mu = F.sum(_gamma * _x_mu_sig, axis=1)
		G_sig = F.sum(_gamma * (_x_mu_sig**2 - 1), axis=1)

		_w = self.xp.broadcast_to(self.w, G_mu.shape)
		G_mu /= self.n_components * self.xp.sqrt(_w)
		G_sig /= self.n_components * self.xp.sqrt(2 * _w)

		# 2 * (n, in_size, n_components) -> (n, in_size, n_components, 2)
		res = F.stack([G_mu, G_sig], axis=-1)
		# res = F.stack([G_mu], axis=-1)
		# (n, in_size, n_components, 2) -> (n, 2*in_size*n_components)
		res = F.reshape(res, (x.shape[0], -1))
		return res

	def __call__(self, x):
		x = super(FVLayer, self).__call__(x)
		return self.encode(x)
