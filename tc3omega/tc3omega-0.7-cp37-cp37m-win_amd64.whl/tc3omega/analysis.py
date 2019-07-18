# !/usr/bin/env python
# -*- coding: utf-8 -*-i
import time
import numpy as np
from .integrators import Integrate_f_a, Integrate_f_i, Integrate_f_s
from .integrators import integrate_f_a, integrate_f_i, integrate_f_s
from scipy.optimize import basinhopping
from scipy.integrate import quad
from cmath import sqrt
sqrt = np.vectorize(sqrt)

"""
INFO

This module is for performing the computations in order to fit the measured
data. For fast calculation, it makes use of the 'calculation' extension, which
is compiled from the Cython module 'calculation.pyx'.
"""


class Analyzer(object):
    def __init__(self, constants, data, kappas, fit_indices,
                 boundary_typ='semi-infinite', use_substrate_guess=False):

        if boundary_typ in ['semi-infinite', 'adiabatic', 'isothermal']:
            pass
        else:
            raise ValueError("invalid 'boundary_typ'")

        self.kappas = kappas
        self.fit_indices = fit_indices
        self.boundary_typ = boundary_typ

        self.name = constants['name']
        self.length = constants['length']
        self.b = constants['half_width']
        self.dRdT = constants['heater_dRdT']
        self.R = constants['R_shunt']
        self.ds = constants['d_values']
        self.Cvs = constants['Cv_values']
        self.layer_names = constants['layer_names']

        self.f_all = data['input_frequencies']
        self.Vs_3w = data['sample_V3w_real']
        self.Vs_1w = data['sample_V1w_real']
        self.Vs_1w_o = data['sample_V1w_imag']
        self.Vsh_1w = data['shunt_V1w_real']
        self.num_points = len(self.f_all)

        self.omegas = 2. * np.pi * self.f_all
        self.ln_omegas = np.log(self.omegas)

        self.use_substrate_guess = use_substrate_guess
        self.substrate_layer = 1  # it's the one right below the film

        # from MC fit using 2D heat transfer
        self.kappa_result = None
        self.N_its = None
        self.equivalent_layers = None

        # from linear approximation
        self.k_film = None
        self.k_sub = None

        self.ps = self.calculate_power()
        self.measured_dTs = self.calculate_measured_dTs()

        self.Integrators_dict = {'adiabatic': Integrate_f_a,
                                 'isothermal': Integrate_f_i,
                                 'semi-infinite': Integrate_f_s}

        self.integrators_dict = {'adiabatic': integrate_f_a,
                                 'isothermal': integrate_f_i,
                                 'semi-infinite': integrate_f_s}

    # ------------------------------------------------------------------------
    # CALCULATIONS
    # NOTE -> assuming sample isotropy for now!!
    # ------------------------------------------------------------------------

    def calculate_power(self):
        """Calculates power dissipation from resistance and 1ω voltage"""
        return (self.Vsh_1w / self.R
                * np.sqrt(self.Vs_1w_o ** 2 + self.Vs_1w ** 2))

    # [T(ω_1), ... , T(ω_n)] calculated from theory
    def calculate_dTs(self, ks):
        """Borca Eq. (1); over all ω values"""
        n = len(ks)
        integrator = self.Integrators_dict[self.boundary_typ]
        result = integrator(
            self.b, self.omegas, self.ds[:n], ks, ks, self.Cvs[:n])

        return -self.ps / (np.pi * self.length * ks[0]) * result
        # TODO: output are exactly the same over all bc...normal?

    # T(ω_i) calculated from theory
    def calculate_dT(self, ks, idx):
        """Borca Eq. (1); at single ω value"""
        n = len(ks)
        integrator = self.integrators_dict[self.boundary_typ]
        result = integrator(
            self.b, self.omegas[idx], self.ds[:n], ks, ks, self.Cvs[:n])

        return -self.ps[idx] / (np.pi * self.length * ks[0]) * result

    def calculate_dTs_LA(self, k_film, k_sub):
        T_sub = (self.ps / (np.pi * self.length * k_sub)
                 * (.5 * np.log(k_sub / self.Cvs[1] / self.b**2)
                    + self.etas - .5 * (np.log(2) + self.ln_omegas)))
        T_film = self.ps * self.ds[0] / (2 * self.b * self.length * k_film)

        return T_sub + T_film

    # ------------------------------------------------------------------------
    # DATA FITTING ALGORITHMS
    # ------------------------------------------------------------------------
    def MCfit2D(self, N=50, equivalent_layers=None,
                minimizer_kwargs={"method": "L-BFGS-B",
                                  "jac": False}):
        # initialize
        t0 = time.time()
        kappas_copy = self.kappas.copy()
        result = self.kappas.copy()

        # calculate best-fit line
        m, b = np.polyfit(self.ln_omegas, self.measured_dTs, 1)

        def fitline(x):
            return m * x + b

        # if each layer gets its own variable
        if equivalent_layers is None:

            # the residual function ------------------------------------------
            def F(_ks):
                np.put(kappas_copy, self.fit_indices, _ks)
                Tws = self.calculate_dTs(kappas_copy)
                res = np.sum(
                    (Tws - fitline(self.ln_omegas)) ** 2) / self.num_points
                return res

            # linnear approximation to get estimates
            if self.use_substrate_guess:
                m = np.polyfit(np.log(self.omegas), self.measured_dTs, 1)[0]
                k_S = -np.mean(self.ps) / (2. * np.pi * self.length * m)
                self.k_S = k_S
                kappas0 = []
                for idx in self.fit_indices:
                    if idx == self.substrate_layer:
                        kappas0.append(k_S)
                    else:
                        kappas0.append(self.kappas[idx])
                kappas0 = np.array([kappas0])
            else:
                kappas0 = np.array([self.kappas[i] for i in self.fit_indices])

            # fit engine
            fit = basinhopping(
                F, kappas0, minimizer_kwargs=minimizer_kwargs, niter=N)
            self.F_last = fit.fun
            np.put(result, self.fit_indices, fit.x)

        # if some layers represented by the same varaible
        else:
            _ks_indices = [x for x in range(len(self.fit_indices))]
            _fit_indices = self.fit_indices.copy()

            for tupl in equivalent_layers:
                assert type(tupl) == tuple
                assert len(tupl) == 2

                swaps = [self.fit_indices.index(idx) for idx in tupl]
                _ks_indices[swaps[1]] = _ks_indices[swaps[0]]

                loc = _fit_indices.index(tupl[1])
                _fit_indices.remove(_fit_indices[loc])

            # TODO: recall the purpose of this loop, sometimes it does nothing
            _ks_ = _ks_indices.copy()
            for i, idx in enumerate(_ks_indices):
                if i != 0 and np.max(_ks_[:i]) < idx:
                    _ks_[i] = np.max(_ks_[:i]) + 1

            # the residual function ------------------------------------------
            def F(_ks):
                np.put(kappas_copy, self.fit_indices, [_ks[i] for i in _ks_])
                Tws = self.calculate_dTs(kappas_copy)
                res = np.sum(
                    (Tws - fitline(self.ln_omegas)) ** 2) / self.num_points
                return res

            kappas0 = np.array([self.kappas[i] for i in _fit_indices])
            if self.use_substrate_guess:
                m = np.polyfit(np.log(self.omegas), self.measured_dTs, 1)[0]
                k_S = -np.mean(self.ps) / (2. * np.pi * self.length * m)
                self.k_S = k_S
                np.put(kappas0, self.substrate_layer, k_S)
            fit = basinhopping(
                F, kappas0, minimizer_kwargs=minimizer_kwargs, niter=N)
            self.F_last = fit.fun
            for i, idx in enumerate(self.fit_indices):
                np.put(result, idx, fit.x[_ks_[i]])

        self.t_calc = time.time() - t0
        self.equivalent_layers = equivalent_layers
        self.kappa_result = result
        self.N_its = N
        return result

    def LinApproxFit(self, const_eta=None):
        # measured T(ln_w) has same slope as T_sub(ln_w)
        m, b = np.polyfit(self.ln_omegas, self.measured_dTs, 1)

        def fitline(x):
            return m * x + b

        # measured T(ln_w) slope is a function of 'k_sub'; invert it
        k_sub = np.mean(-self.ps / (2. * np.pi * self.length * m))

        # to calculate 'eta' from Seung-Min Lee's integral formula
        if const_eta is None:
            def eta(w):
                intg_f = quad(
                    lambda x, w: ((np.sin(x * self.b) / (x * self.b))**2
                                  * 1 / sqrt(x**2 + 1j * self.q(w)**2)).real,
                    1, 1e8, args=(w,), limit=1000
                )
                return intg_f[0] + np.log(self.q(w) * self.b)

            self.etas = np.array([eta(w) for w in self.omegas])
        else:
            self.etas = const_eta

        T_sub = (self.ps / (np.pi * self.length * k_sub)
                 * (.5 * np.log(k_sub / self.Cvs[1] / self.b**2)
                    + self.etas - .5 * (np.log(2) + self.ln_omegas)))

        T_film = fitline(self.ln_omegas) - T_sub
        k_film = np.mean(
            (self.ps / self.length) * self.ds[0] / T_film / (2. * self.b))

        self.k_sub = k_sub
        self.k_film = k_film
        return k_film, k_sub
    # ------------------------------------------------------------------------
    # UTILITIES
    # ------------------------------------------------------------------------

    def calculate_measured_dTs(self):
        return -2. * self.Vs_3w / ((self.Vsh_1w / self.R) * self.dRdT)

    def q(self, w):
        return np.sqrt(2. * w * self.Cvs[1] / self.kappas[1])
