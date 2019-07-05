#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy.optimize import basinhopping
from .integrators import integrate_f_a, integrate_f_i, integrate_f_s
from .integrators import Integrate_f_a, Integrate_f_i, Integrate_f_s
import numpy as np
import time

"""
INFO

This module is for performing the computations in order to fit the measured
data. For fast calculation, it makes use of the 'calculation' extension, which
is compiled from the Cython module 'calculation.pyx'.
"""


class Analyzer(object):
    def __init__(self, constants, data, kappas, fit_indices, boundary_typ,
                 substrate_layer=None, use_substrate_guess=False):
        self.name = constants['name']
        self.length = constants['length']
        self.b = constants['half_width']
        self.dRdT = constants['heater_dRdT']
        self.R = constants['R_shunt']
        self.ds = constants['d_values']
        self.Cvs = constants['Cv_values']
        self.layer_names = constants['layer_names']

        self.f_all = data['input_frequencies']
        self.omegas = 2 * np.pi * self.f_all
        self.Vs_3w = data['real_sample_V3ω']
        self.Vs_1w = data['real_sample_V1ω']
        self.Vs_1w_o = data['imag_sample_V1ω']
        self.Vsh_1w = data['real_shunt_V1ω']
        self.num_points = self.f_all.shape[0]

        self.kappas = kappas
        self.fit_indices = fit_indices
        self.boundary_typ = boundary_typ
        self.substrate_layer = substrate_layer
        self.use_substrate_guess = use_substrate_guess

        self.ps = self.calculate_power()
        self.target_dTs = self.measured_dTs()

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

    # all ω values
    def Fit_dT(self, ks):
        """Borca Eq. (1); over all ω values"""
        integrator = self.Integrators_dict[self.boundary_typ]
        result = integrator(self.b, self.omegas, self.ds, ks, ks, self.Cvs)

        return -self.ps / (np.pi * self.length * ks[0]) * result
        # TODO: output are exactly the same over all bc...normal?

    # only ω = self.omegas[idx]
    def fit_dT(self, ks, idx):
        """Borca Eq. (1); at single ω value"""
        integrator = self.integrators_dict[self.boundary_typ]
        result = integrator(self.b, self.omegas[idx],
                            self.ds, ks, ks, self.Cvs)

        return -self.ps[idx] / (np.pi * self.length * ks[0]) * result

    # ------------------------------------------------------------------------
    # DATA FITTING ALGORITHMS
    # ------------------------------------------------------------------------
    def MC_fit_dT(self, idx, N, equivalent_layers=None,
                  minimizer_kwargs={"method": "L-BFGS-B",
                                    "jac": False}):
        t0 = time.time()
        kappas_copy = self.kappas.copy()
        result = self.kappas.copy()

        if equivalent_layers is None:
            def F(_ks):
                np.put(kappas_copy, self.fit_indices, _ks)
                Tw = self.fit_dT(kappas_copy, idx)
                return abs(Tw - self.target_dTs[idx])
            kappas0 = np.array([self.kappas[i] for i in self.fit_indices])
            ret = basinhopping(F, kappas0, minimizer_kwargs=minimizer_kwargs,
                               niter=N)
            np.put(result, self.fit_indices, ret.x)

        else:
            _ks_indices = np.array(range(len(self.fit_indices)))
            _fit_indices = np.array(self.fit_indices)
            for tupl in equivalent_layers:
                assert type(tupl) is tuple
                assert len(tupl) == 2
                np.put(_ks_indices, tupl[1]-1, _ks_indices[tupl[0]-1])
                _fit_indices = np.delete(_fit_indices, tupl[1]-1)

            _ks_ = _ks_indices.copy()
            for i, idx in enumerate(_ks_indices):
                if i != 0 and np.max(_ks_[:i]) < idx:
                    _ks_[i] = np.max(_ks_[:i]) + 1

            def F(_ks):
                np.put(kappas_copy, self.fit_indices,
                       [_ks[i] for i in _ks_])
                Tw = self.fit_dT(kappas_copy, idx)
                return abs(Tw - self.target_dTs[idx])
            kappas0 = np.array([self.kappas[i]
                                for i in _fit_indices])

            if self.use_substrate_guess:
                m = np.polyfit(np.log(self.omegas), self.target_dTs, 1)[0]
                k_S = -np.mean(self.ps) / (2 * np.pi * self.length * m)
                np.put(kappas0, self.substrate_layer-1, k_S)
            ret = basinhopping(F, kappas0, minimizer_kwargs=minimizer_kwargs,
                               niter=N)
            for idx in self.fit_indices:
                np.put(result, idx, ret.x[_ks_[idx]])
        self.t_calc = time.time() - t0
        return result

    def MC_fitlinear_dT(self, idx, N=50, equivalent_layers=None,
                        minimizer_kwargs={"method": "L-BFGS-B",
                                          "jac": False}):
        t0 = time.time()
        kappas_copy = self.kappas.copy()
        result = self.kappas.copy()
        m, b = np.polyfit(np.log(self.omegas), self.target_dTs, 1)

        def fitline(x):
            return m * x + b

        if equivalent_layers is None:
            def F(_ks):
                np.put(kappas_copy, self.fit_indices, _ks)
                Tw = self.fit_dT(kappas_copy, idx)
                return abs(Tw - fitline(np.log(self.omegas[idx])))

            if self.use_substrate_guess:
                m = np.polyfit(np.log(self.omegas), self.target_dTs, 1)[0]
                k_S = -np.mean(self.ps) / (2 * np.pi * self.length * m)
                kappas0 = []
                for idx in self.fit_indices:
                    if idx == self.substrate_layer-1:
                        kappas0.append(k_S)
                    else:
                        kappas0.append(self.kappas[idx])
                kappas0 = np.array([kappas0])
            else:
                kappas0 = np.array([self.kappas[i] for i in self.fit_indices])

            ret = basinhopping(
                F, kappas0, minimizer_kwargs=minimizer_kwargs, niter=N)
            np.put(result, self.fit_indices, ret.x)

        else:
            _ks_indices = [x for x in range(len(self.fit_indices))]
            _fit_indices = self.fit_indices.copy()

            for tupl in equivalent_layers:
                assert type(tupl) == tuple
                assert len(tupl) == 2

                new_tupl = (tupl[0]-1, tupl[1]-1)

                swaps = [self.fit_indices.index(idx) for idx in new_tupl]
                _ks_indices[swaps[1]] = _ks_indices[swaps[0]]

                loc = _fit_indices.index(new_tupl[1])
                _fit_indices.remove(_fit_indices[loc])

            # TODO: recall the purpose of this loop, sometimes it does nothing
            _ks_ = _ks_indices.copy()
            for i, idx in enumerate(_ks_indices):
                if i != 0 and np.max(_ks_[:i]) < idx:
                    _ks_[i] = np.max(_ks_[:i]) + 1

            def F(_ks):
                np.put(kappas_copy, self.fit_indices, [_ks[i] for i in _ks_])
                Tw = self.fit_dT(kappas_copy, idx)
                return abs(Tw - fitline(np.log(self.omegas[idx])))

            kappas0 = np.array([self.kappas[i] for i in _fit_indices])
            if self.use_substrate_guess:
                m = np.polyfit(np.log(self.omegas), self.target_dTs, 1)[0]
                k_S = -np.mean(self.ps) / (2 * np.pi * self.length * m)
                np.put(kappas0, self.substrate_layer-1, k_S)
            ret = basinhopping(
                F, kappas0, minimizer_kwargs=minimizer_kwargs, niter=N)

            for i, idx in enumerate(self.fit_indices):
                np.put(result, idx, ret.x[_ks_[i]])

        self.t_calc = time.time() - t0
        return result

    # ------------------------------------------------------------------------
    # UTILITIES
    # ------------------------------------------------------------------------

    def measured_dTs(self):
        return -2 * self.Vs_3w / ((self.Vsh_1w / self.R) * self.dRdT)
