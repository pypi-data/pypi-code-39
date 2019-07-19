import chainer
from chainer.backends import cuda
from chainer import link
from chainer import initializers
from chainer import functions as F

import os
import numpy as np

from os.path import join, isdir

class GMMLayer(link.Link):

	def __init__(self, in_size, n_components,
		init_mu=None, init_sig=1,
		init_from_data=False,
		alpha=0.9, eps=1e-6,
		dtype=np.float32):

		super(GMMLayer, self).__init__()

		self.n_components = n_components
		self.in_size = in_size

		self.i = 0
		self.lim = 1
		self.visualization_interval = 100
		self.visualization_folder = "mu_change"

		if init_mu is None:
			self.init_mu = initializers.Uniform(scale=1, dtype=dtype)

		elif isinstance(init_mu, (int, float)):
			self.init_mu = initializers.Uniform(scale=init_mu, dtype=dtype)

		elif isinstance(init_mu, (np.ndarray, chainer.cuda.ndarray)):
			self.init_mu = initializers.Constant(init_mu, dtype=dtype)

		elif not isinstance(init_mu, chainer.initializer.Initializer):
			raise ValueError(
				"\"init_mu\" should be either omited, be an instance of " + \
				"chainer.initializer.Initializer or a numpy/cupy array!"
			)


		self.init_sig = initializers.Constant(init_sig, dtype=dtype)
		self.init_w = initializers.Constant(1 / n_components, dtype=dtype)
		self._initialized = False

		with self.init_scope():
			self.add_persistent("mu",
				np.zeros((self.in_size, self.n_components), dtype))

			self.add_persistent("sig",
				np.zeros((self.in_size, self.n_components), dtype))

			self.add_persistent("w",
				np.zeros((self.n_components), dtype))

			self.add_persistent("alpha", alpha)
			self.add_persistent("eps", eps)
			self.add_persistent("t", 1)

			if not init_from_data:
				self.init_params()

	def reset(self):
		self.t = 1

	def init_params(self):
		self.init_mu(self.mu)
		self.init_sig(self.sig)
		self.init_w(self.w)
		self._initialized = True

	def init_from_data(self, x):
		from sklearn.mixture import GaussianMixture

		if isinstance(x, chainer.Variable):
			data = cuda.to_cpu(x.array)
		else:
			data = cuda.to_cpu(x)

		gmm = GaussianMixture(
			n_components=self.n_components,
			covariance_type="diag",
		)

		gmm.fit(data.reshape(-1, data.shape[-1]))

		self.mu[:]  = self.xp.array(gmm.means_.T)
		self.sig[:] = self.xp.array(gmm.covariances_.T)
		self.w[:]   = self.xp.array(gmm.weights_)

		self._initialized = True


	def _check_input(self, x):
		assert x.ndim == 3, \
			"input should have following dimensions: (batch_size, n_features, feature_size)"
		n, t, in_size = x.shape
		assert in_size == self.in_size, \
			f"feature size of the input does not match input size: ({in_size} != {self.in_size})! "
		return n, t

	def _expand_params(self, x):
		n, t = self._check_input(x)
		shape = (n, t, self.in_size, self.n_components)
		shape2 = (n, t, self.n_components)

		_x = F.broadcast_to(F.expand_dims(x, -1), shape)

		_params = [(self.mu, shape), (self.sig, shape), (self.w, shape2)]
		_mu, _sig, _w = [
			F.broadcast_to(F.expand_dims(F.expand_dims(p, 0), 0), s)
				for p, s in _params]

		return _x, _mu, _sig, _w

	def log_soft_assignment(self, x):

		_log_proba, _w = self.log_proba(x, weighted=False)
		_log_wu = _log_proba + F.log(_w)

		_log_wu_sum = F.logsumexp(_log_wu, axis=-1)
		_log_wu_sum = F.expand_dims(_log_wu_sum, axis=-1)
		_log_wu_sum = F.broadcast_to(_log_wu_sum, _log_wu.shape)

		return _log_wu - _log_wu_sum

	def log_proba(self, x, weighted=False):
		_x, _mu, _sig, _w = self._expand_params(x)

		_dist = (_x - _mu) / _sig
		_dist = F.sum(_dist**2, axis=2)
		_log_proba = -_dist / 2

		if weighted:
			_log_wu = _log_proba + F.log(_w)
			_log_proba = F.logsumexp(_log_wu, axis=-1)

		return _log_proba, _w

	def soft_assignment(self, *args, **kwargs):
		return F.exp(self.log_soft_assignment(*args, **kwargs))

	def proba(self, *args, **kwargs):
		_log_proba, _w = self.log_proba(*args, **kwargs)
		return F.exp(_log_proba), _w

	def __call__(self, x):
		if chainer.config.train:
			self.update_parameter(x)
		return x

	def _ema(self, old, new):
		prev_correction = 1 - (self.alpha ** (self.t-1))
		correction = 1 - (self.alpha ** self.t)

		uncorrected_old = old * prev_correction
		res = self.alpha * uncorrected_old + (1 - self.alpha) * new

		return res / correction

	def update_parameter(self, x):
		if not self._initialized:
			self.init_from_data(x)

		if self.alpha >= 1:
			return

		self.t += 1

		## E-Step ##
		gamma = self.soft_assignment(x)
		n, t, n_components = gamma.shape

		## M-Step ##
		N_K = gamma.array.sum(axis=(0, 1))
		N_K = self.xp.maximum(N_K, self.eps)

		# compute new weights
		new_w =  N_K / N_K.sum()
		self.w[:] = self._ema(self.w, new_w)

		# compute new mus
		shape = (n, t, self.in_size, self.n_components)
		_x = F.broadcast_to(F.expand_dims(x, axis=3), shape)
		_gamma = F.broadcast_to(F.expand_dims(gamma, axis=2), shape)

		new_mu = (_x * _gamma).array.sum(axis=(0, 1)) / N_K
		self.mu[:]  = self._ema(self.mu, new_mu)

		# compute new sigmas
		###### estimating sigma does not work yet! ######
		# _dist = (_x - new_mu)**2
		# new_sig = (_dist * _gamma).array.sum(axis=(0, 1)) / N_K
		# self.sig[:] = self._ema(self.sig, self.xp.sqrt(new_sig))

		# self.i += 1
		# if (self.i-1) % self.visualization_interval == 0:
		# 	self.__visualize(x, gamma, new_mu, None, new_w)

	def __visualize(self, x, soft_assignment, *new_params):
		import matplotlib.pyplot as plt
		mu, sig, w = new_params

		fig, ax = plt.subplots()

		data = cuda.to_cpu(x.array).reshape(-1, x.shape[-1])
		data_col = cuda.to_cpu(soft_assignment.array).argmax(axis=-1).reshape(-1)
		xs, ys = data.T
		cmap = plt.cm.jet

		ax.scatter(xs, ys, alpha=0.6, c=data_col, cmap=cmap)
		_new_mus, _old_mus = cuda.to_cpu(mu), cuda.to_cpu(self.mu)

		# ax.scatter(*_new_mus, marker="x", c="black")
		# ax.scatter(*_old_mus, marker="o", c="red")

		for i, ((x0, y0), (x1, y1)) in enumerate(zip(_new_mus.T, _old_mus.T)):
			col = np.array(cmap(i / self.n_components))

			ax.scatter(x0, y0, marker="x", c=col.reshape(1,-1))
			ax.scatter(x1, y1, marker="D", c=col.reshape(1,-1))

			ax.plot([x0, x1], [y0, y1], c=col)


		self.lim = max(self.lim, float(self.xp.abs(x.array).max())*1.05)
		ax.set_xlim(-self.lim, self.lim)
		ax.set_ylim(-self.lim, self.lim)

		if not isdir(self.visualization_folder):
			os.makedirs(self.visualization_folder)

		ax.set_title(f"Iteration {self.i:06d}")
		plt.tight_layout()
		fig.savefig(join(self.visualization_folder, f"iteration_{self.i:06d}.png"))

		# plt.show()
		plt.close()
		# import pdb; pdb.set_trace()
