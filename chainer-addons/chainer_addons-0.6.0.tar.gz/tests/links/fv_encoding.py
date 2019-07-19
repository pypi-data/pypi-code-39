import numpy as np

from unittest import TestCase, skip

import chainer
import chainer.functions as F


from chainer_addons.links.fisher_encoding import GMMLayer


class GMMLayerTest(TestCase):

	def __init__(self, *args, **kwargs):
		super(GMMLayerTest, self).__init__(*args, **kwargs)
		self.xp = np

		self.n, self.t, self.in_size = 2, 3, 512
		self.n_components = 4
		self.alpha = 0.9

		self.seed = 89314567
		self.dtype = np.float32


	def setUp(self):
		rnd = self.xp.random.RandomState(self.seed)

		X = rnd.randn(self.n, self.t, self.in_size).astype(self.dtype)
		self.X = chainer.Variable(X)

		self.init_mu = rnd.randn(self.in_size, self.n_components).astype(self.dtype)
		# self.init_mu = self.xp.ones((self.in_size, self.n_components), self.dtype)

	def _new_layer(self, init_mu=None, init_sig=1):
		return GMMLayer(
			self.in_size,
			self.n_components,
			init_mu=self.init_mu if init_mu is None else init_mu,
			init_sig=init_sig,
			alpha=self.alpha)

	def test_assignment(self):
		layer = self._new_layer()

		gamma = layer.soft_assignment(self.X).array
		correct_shape = (self.n, self.t, self.n_components)
		self.assertEqual(gamma.shape, correct_shape,
			"Shape of the soft assignment is not correct!")

		gamma_sum = gamma.sum(axis=-1)
		self.assertTrue(np.allclose(gamma_sum, 1, atol=1e-5),
			"Sum of the soft assignment should be always equal to 1, but was: \n"+\
			f"{gamma_sum}")

	def test_update(self):
		layer = self._new_layer()
		params = (layer.mu, layer.sig, layer.w)

		params0 = [np.copy(p) for p in params]
		with chainer.using_config("train", False):
			y0 = layer(self.X)
		params1 = [np.copy(p) for p in params]

		for p0, p1 in zip(params0, params1):
			self.assertTrue(np.all(p0 == p1),
				"Params should not be updated when not training!")


		params0 = [np.copy(p) for p in params]
		with chainer.using_config("train", True):
			y0 = layer(self.X)
		params1 = [np.copy(p) for p in params]

		for p0, p1 in zip(params0, params1):
			self.assertTrue(np.all(p0 != p1),
				"Params should be updated when training!")


