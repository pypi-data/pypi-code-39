#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tc3omega.datareader import Data
from tc3omega.constants import Constants
from tc3omega.analysis import Analyzer
from tc3omega.logmaker import Logmaker

import unittest
import shutil
import os
import numpy as np

kappas = np.array([1.4, 130, 1.4, 0.5, 205], dtype=np.double)
fit_indices = [0, 1, 2]
boundary_typ = 'adiabatic'
substrate_layer = 2  # user input, maps to index 1
use_substrate_guess = True
equivalent_layers = [(1, 3)]  # user input, maps to indices (0, 2)
N_its = 50

cwd = os.getcwd()


class TestRunExample(unittest.TestCase):
    def setUp(self):
        self.constants = Constants.fromFile(
            cwd + "/tc3omega/example/sample_file_example.yml").getvals()
        self.data = Data(cwd + "/tc3omega/example/measured_data_example.csv")

    def test_run_and_log_analyzer(self):
        A = Analyzer(self.constants, self.data,
                     kappas, fit_indices, boundary_typ, substrate_layer,
                     use_substrate_guess)

        kappa_result = A.MC_fitlinear_dT(
            int(A.num_points/2), equivalent_layers=equivalent_layers)

        logger = Logmaker(A, kappa_result, N_its, equivalent_layers)

        logger.make_log()
        logger.make_plot()

        output_dir = logger.make_output_dir()
        abspath_to_log_dir = "/".join([cwd, output_dir])

        # Clean up
        shutil.rmtree(abspath_to_log_dir)
