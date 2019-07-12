# -*- coding: utf-8 -*-

"""
This module implements tracking control by approximative linearization
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



# test tracking control
l = 1.
g = 9.81
x1, x2, x3, x4 = xx = st.symb_vector("x1:5")
u1,  = uu = st.symb_vector("u1:2")
ff_o = sp.Matrix([x3, x4, 0, -g/l*sin(x2)])
gg_o = sp.Matrix([ 0,  0, 1, -1/l*cos(x2)])

A = ff_o.jacobian(xx).subz0(xx)
bb = gg_o.subz0(xx)

ffl = A*xx
ggl = bb


if 0:
    ff = ffl
    gg = ggl
else:
    ff = ff_o
    gg = gg_o

clcp_coeffs = st.coeffs((x1 + 2) ** 4)[::-1]


if 0:
    ff2 = st.multi_taylor_matrix(ff, xx, x0=[0]*4, order=2)
    gg2 = st.multi_taylor_matrix(gg, xx, x0=[0]*4, order=2)

    feedback_gain_func = feedback_factory(ff, gg, xx, clcp_coeffs)
    # feedback_gain_func(xx0)

mod1 = st.SimulationModel(ff, gg, xx)

detQc = st.nl_cont_matrix(ff, gg, xx, n_extra_cols=0).berkowitz_det()
detQc_func = sp.lambdify(xx, detQc, modules="numpy")


# calculate ref-input for swingup:

ffl = sp.lambdify(list(xx)+list(uu), list(ff+gg*u1), modules=["sympy"])


def pytraj_f(xx, uu, uuref, t, pp):

    args = list(xx) + list(uu)
    return ffl(*args)


from pytrajectory import TransitionProblem
from pytrajectory import log, aux
log.console_handler.setLevel(40)

a = 0.0
xa = [0.0, 0.0, 0.0, 0.0]

b = 3.0
xb = [0.0, np.pi, 0.0, 0.0]

ua = [0.0]
ub = [0.0]

Tend = b + 0  # ensure meaningfull input if increasing


pfname = "swingup_splines.pcl"
if 1:
    first_guess = {'seed': 20}
    S = TransitionProblem(pytraj_f, a, b, xa, xb, ua, ub, first_guess=first_guess, kx=2, eps=5e-2,
                          use_chains=False) # , sol_steps=1300

    # time to run the iteration
    solC = S.solve(return_format="info_container")

    cont_dict = aux.containerize_splines(S.eqs.trajectories.splines)

    with open(pfname, "wb") as pfile:
        pickle.dump(cont_dict, pfile)

else:
    with open(pfname, "rb") as pfile:
        cont_dict = pickle.load(pfile)

xxf, uuf = aux.get_xx_uu_funcs_from_containerdict(cont_dict)

tt = np.linspace(uuf.a, uuf.b, 10000)

xx_values = np.array([xxf(t) for t in tt])
uu_values = np.array([uuf(t) for t in tt])

xxuu_values = np.c_[tt, xx_values, uu_values]
np.savez("cart_pend_sup_3.npz", tt, xx_values, uu_values)

IPS()

exit()
