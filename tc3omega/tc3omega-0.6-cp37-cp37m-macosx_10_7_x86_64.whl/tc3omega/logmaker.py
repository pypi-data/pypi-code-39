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
    def __init__(self, AnalyzerObj, kappa_result, N, equivalent_layers):
        self.A = AnalyzerObj
        self.kappa_result = kappa_result
        self.N = N
        self.equivalent_layers = equivalent_layers
        self.cwd = os.getcwd()
        self._dir_name = '_fit_results' + '(' + AnalyzerObj.boundary_typ + ')'

        self.fitted_dTs = AnalyzerObj.Fit_dT(kappa_result)
        self.target_dTs = AnalyzerObj.target_dTs
        self.fit_vs_target_dT_residual = (1 / self.target_dTs.shape[0]
                                          * np.sum(
            (self.target_dTs - self.fitted_dTs) ** 2))

    def make_output_dir(self):
        output_dir = self.A.name + self._dir_name
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
            file.write("fit residual vs. measured data: {}"
                       .format(self.fit_vs_target_dT_residual) + "\n")
            file.write("calculation time: {:.2f} (s)"
                       .format(self.A.t_calc) + "\n")
        return

    def make_plot(self):
        output_dir = self.make_output_dir()
        filename = '_(' + self.A.boundary_typ + ')' + '_plot.PNG'
        path = "/".join([output_dir, self.A.name + filename])
        X = np.log(self.A.omegas)

        m, b = np.polyfit(X, self.A.target_dTs, 1)

        def fitline(x):
            return m * x + b

        plt.figure()
        plt.plot(X, self.A.target_dTs, '^', label='measured')
        plt.plot(X, self.fitted_dTs, linewidth=1,
                 label=' '.join(['fit', self.A.boundary_typ]))
        plt.plot(X, fitline(X), ':', linewidth=0.5, label='best-fit line')

        plt.title('sample name: {}'.format(self.A.name))
        plt.xlabel(r'$\ln(\omega)$')
        plt.ylabel(r'Temperature rise, $T$ [K]')
        plt.legend()
        plt.savefig(path, dpi=250)
        return
