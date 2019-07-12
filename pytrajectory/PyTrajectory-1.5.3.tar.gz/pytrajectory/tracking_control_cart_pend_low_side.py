# -*- coding: utf-8 -*-

"""
calculate trajectory for side-stepping (low)
"""

from __future__ import print_function

import numpy as np
import sympy as sp
import time
import sys
import pickle
from matplotlib import pyplot as plt

import symbtools as st

from sympy import sin, cos
from scipy.integrate import odeint
from scipy.interpolate import interp1d

import scipy as sc
from ipydex import IPS, activate_ips_on_exception
from sympy_to_c import sympy_to_c as sp2c

activate_ips_on_exception()


if sys.version_info[0] == 2:
    FileNotFoundError = IOError



l = 5.
g = 9.81
x1, x2, x3, x4 = xx = st.symb_vector("x1:5")
u1,  = uu = st.symb_vector("u1:2")
ff = ff_o = sp.Matrix([x3, x4, 0, -g/l*sin(x2)])
gg = gg_o = sp.Matrix([ 0,  0, 1, -1/l*cos(x2)])

A = ff_o.jacobian(xx).subz0(xx)
bb = gg_o.subz0(xx)


# calculate ref-input for swingup:

ffl = sp.lambdify(list(xx)+list(uu), list(ff+gg*u1), modules=["sympy"])


def pytraj_f(xx, uu, uuref, t, pp):

    args = list(xx) + list(uu)
    return ffl(*args)


from pytrajectory import TransitionProblem
from pytrajectory import log, aux
log.console_handler.setLevel(10)

a = 0.0
xa = [0.0, 0.0, 0.0, 0.0]

b = 4.0
xb = [10, 0, 0.0, 0.0]

ua = [0.0]
ub = [0.0]

Tend = b + 0  # ensure meaningfull input if increasing


first_guess = {'seed': 1}
con = {'x1': [-0.1, 13.5],
       'x3': [-6, 18]}
# con = {'x1': [-0.1, 5.5],
       # 'x3': [-1, 6]}
S = TransitionProblem(pytraj_f, a, b, xa, xb, ua, ub, first_guess=first_guess, kx=2, eps=5e-4,
                      constraints=con,
                      use_chains=False)  # , sol_steps=1300

# time to run the iteration
solC = S.solve(return_format="info_container")

cont_dict = aux.containerize_splines(S.eqs.trajectories.splines)

# fehlerbehaftet bei constraints?:
# xxf, uuf = aux.get_xx_uu_funcs_from_containerdict(cont_dict)
#
# tt = np.linspace(uuf.a, uuf.b, 100)
#
# xx_values = np.array([xxf(t) for t in tt])
# uu_values = np.array([uuf(t) for t in tt])

# xxuu_values = np.c_[tt, xx_values, uu_values]
fname = "cart_pend_side_4_xx.npz"
np.savez(fname, S.sim_data_tt, S.sim_data_xx, S.sim_data_uu)

xx_values = S.sim_data_xx*1

xx_values[:, 1] *= 180/np.pi

plt.plot(S.sim_data_tt, xx_values[:, :2])
plt.show()
IPS()

exit()
