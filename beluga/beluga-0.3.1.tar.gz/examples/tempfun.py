from beluga.bvpsol import spbvp, Shooting
from beluga.ivpsol import Trajectory
import numpy as np
import matplotlib.pyplot as plt

import time

const = 1e-1

narcs = np.arange(1, 512, 1)
times = np.zeros(narcs.shape)

def odefun(X, u, p, const):
    return X[1], X[1] / const[0]

def bcfun(X0, q0, u0, Xf, qf, uf, p, ndp, const):
    return X0[0] - 1, Xf[0]


for ii, N in enumerate(narcs):
    algo = Shooting(odefun, None, bcfun, num_arcs=N)
    solinit = Trajectory()
    solinit.t = np.linspace(0, 1, 2)
    solinit.y = np.array([[0, 1], [0, 1]])
    solinit.const = np.array([const])
    t0 = time.time()
    sol1 = algo.solve(solinit)
    t1 = time.time()
    times[ii] = t1-t0
    print(N)

plt.plot(narcs, times)
plt.show()

np.save('dense', np.vstack((narcs, times)))
