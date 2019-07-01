from tools import utils, matrix, data
import scprep
import pandas as pd
import numpy as np
from sklearn.utils.testing import assert_warns_message, assert_raise_message
from scipy import sparse
from functools import partial
import unittest


class TestGeneSetExpression(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.X_dense = data.load_10X(sparse=False)
        self.X_sparse = data.load_10X(sparse=True)
        self.Y = scprep.measure.gene_set_expression(self.X_dense,
                                                    genes="Arl8b")

    def test_setup(self):
        assert self.Y.shape[0] == self.X_dense.shape[0]
        utils.assert_all_equal(self.Y, scprep.select.select_cols(
            self.X_dense, idx="Arl8b"))

    def test_single_pandas(self):
        matrix.test_pandas_matrix_types(
            self.X_dense, utils.assert_transform_equals,
            Y=self.Y, transform=scprep.measure.gene_set_expression,
            genes="Arl8b")

    def test_array_pandas(self):
        matrix.test_pandas_matrix_types(
            self.X_dense, utils.assert_transform_equals,
            Y=self.Y, transform=scprep.measure.gene_set_expression,
            genes=["Arl8b"])

    def test_starts_with_pandas(self):
        matrix.test_pandas_matrix_types(
            self.X_dense, utils.assert_transform_equals,
            Y=self.Y, transform=scprep.measure.gene_set_expression,
            starts_with="Arl8b")

    def test_single_all(self):
        matrix.test_all_matrix_types(
            self.X_dense, utils.assert_transform_equals,
            Y=self.Y, transform=scprep.measure.gene_set_expression,
            genes=0)

    def test_array_all(self):
        matrix.test_all_matrix_types(
            self.X_dense, utils.assert_transform_equals,
            Y=self.Y, transform=scprep.measure.gene_set_expression,
            genes=[0])
