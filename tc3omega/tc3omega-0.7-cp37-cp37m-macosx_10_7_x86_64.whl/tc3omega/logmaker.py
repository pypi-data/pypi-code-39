#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from tc3omega import __version__

"""
INFO

This module makes the fit log and plots the fitted data, measured data, and
line of best fit.
"""


def sigdig_parse(num_val):
    num_str = str(num_val)
    tmp = num_str.split('.')
    new_num_str = '.'.join([tmp[0], tmp[1][:2] + "(" + tmp[1][2:] + ")"])
    return new_num_str


class Logmaker(object):
    def __init__(self, AnalyzerObj):
        self.A = AnalyzerObj
        self.kappa_result = AnalyzerObj.kappa_result
        self.N = AnalyzerObj.N_its
        self.equivalent_layers = AnalyzerObj.equivalent_layers
        self.cwd = os.getcwd()
        self._dir_name = '(fit_results-' + AnalyzerObj.boundary_typ + ')_'
        self.measured_dTs = AnalyzerObj.measured_dTs

    def make_output_dir(self):
        output_dir = self._dir_name + self.A.name
        try:
            os.mkdir(output_dir)
        except FileExistsError:
            pass
        return output_dir

    def print_dir_info(self):
        cwd = os.getcwd()
        output_dir = self.make_output_dir()
        abspath_to_log_dir = "/".join([cwd, output_dir])
        print()
        print("wrote fit results to -> {}".format(abspath_to_log_dir))
        print()

    def make_log(self):
        output_dir = self.make_output_dir()
        path = "/".join([output_dir, self.A.name + '_LOG.txt'])
        now = datetime.now()
        with open(path, mode='w') as file:
            file.write("(tc3omega version {}".format(__version__)
                       + " | " + now.strftime("%Y-%m-%d %H:%M:%S") + ")"
                       + "\n")
            file.write("\n")
            file.write("initial guess: {}".format(self.A.kappas) + "\n")
            file.write("\n")
            file.write("THERMAL CONDUCTIVITIES [W/m/K]" + "\n")
            file.write("------------------------------" + "\n")
            for i, layer_name in enumerate(self.A.layer_names):
                file.write(("{}: {} (*)" if i in self.A.fit_indices
                            else "{}: {}")
                           .format(layer_name,
                                   sigdig_parse(self.kappa_result[i])) + "\n")
            file.write("\n")
            file.write("(* --> fitted value)" + "\n")
            file.write("\n")
            file.write("equivalent layers: {}"
                       .format(self.equivalent_layers) + "\n")
            file.write("substrate guess used: {}".
                       format("yes" if self.A.use_substrate_guess else "no")
                       + "\n")
            file.write("boundary type: {}".format(self.A.boundary_typ) + "\n")
            file.write("number of iterations: {}".format(self.N) + "\n")
            file.write("fit residual: {}"
                       .format(self.A.F_last) + "\n")
            file.write("calculation time: {:.2f} (s)"
                       .format(self.A.t_calc) + "\n")
            file.write("linear approximation guess for substrate: {}"
                       .format(
                           "not used" if self.A.k_S is None else self.A.k_S)
                       + "\n")
            file.write(
                "  number of frequencies: {}".format(self.A.num_points) + "\n")
            file.write("  smallest frequency: {}".format(self.A.min_f) + "\n")
            file.write("  largest frequency: {}".format(self.A.max_f) + "\n")
        return

    def make_MCfit_plot(self, save_plot=False):
        try:
            assert self.A.kappa_result is not None
        except AssertionError:
            print("must run 'Analyzer.MCfit2D()' before making plot")
            return

        fitted_dTs = self.A.calculate_dTs(self.A.kappa_result)
        X = self.A.ln_omegas
        m, b = np.polyfit(X, self.A.measured_dTs, 1)

        def fitline(x):
            return m * x + b

        plt.figure()
        plt.plot(X, self.A.measured_dTs, '^', markersize=8,
                 label='measured')
        plt.plot(X, fitted_dTs, ':', linewidth=1, color='g',
                 marker='o', markersize=8, markerfacecolor='none',
                 markeredgecolor='g',
                 label=' '.join(['2D fit', self.A.boundary_typ]))
        plt.plot(X, fitline(X),
                 linewidth=0.2, color='b', label='data best-fit line')

        plt.title('sample name: {}'.format(self.A.name))
        plt.xlabel(r'$\ln(\omega)$')
        plt.ylabel(r'Temperature rise, $T$ [K]')
        plt.legend()
        if save_plot:
            output_dir = self.make_output_dir()
            filename = '_(' + self.A.boundary_typ + ')' + '_plot.PNG'
            path = "/".join([output_dir, self.A.name + filename])
            plt.savefig(path, dpi=250)
        return

    def make_LAfit_plot(self, save_plot=False):
        try:
            assert self.A.k_film is not None
            assert self.A.k_sub is not None
        except AssertionError:
            print("must run 'Analyzer.LinApproxFit()' before making plot")
            return

        dTs_LA = self.A.calculate_dTs_LA(self.A.k_film, self.A.k_sub)

        X = self.A.ln_omegas
        plt.figure()
        plt.plot(X, self.A.measured_dTs, '^', label='measured')
        plt.plot(X, dTs_LA, ':', linewidth=1, color='r',
                 marker='o', markersize=8, markerfacecolor='none',
                 markeredgecolor='r', label='lin.approx. fit')

        plt.title('sample name: {}'.format(self.A.name)
                  + ', ' + r'$\langle\eta\rangle$ = {:.3f}'
                  .format(np.mean(self.A.etas)))
        plt.xlabel(r'$\ln(\omega)$')
        plt.ylabel(r'Temperature rise, $T$ [K]')
        plt.legend()
        if save_plot:
            output_dir = self.make_output_dir()
            filename = '_(' + self.A.boundary_typ + ')' + '_LA_plot.PNG'
            path = "/".join([output_dir, self.A.name + filename])
            plt.savefig(path, dpi=250)
        return
