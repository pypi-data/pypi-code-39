# -*- coding: utf-8 -*-

# Copyright 2019, Grid.
#
# This source code is licensed under the ReNom Subscription Agreement, version 1.0.
# ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)


import numpy as np
import scipy.spatial
import matplotlib.pyplot as plt

from renom_q.exception import ReNomQError
from .qaa import QAA


class QClustering(QAA):
    """ Quantum Clustering

    Args:
        set_qasm (boolean):
            If it is true, qasm code is added to the calculation result.
            Defaults to False.

    Example:
        >>> import renom_q.ml.qclustering
        >>> qcl = renom_q.ml.qclustering.QClustering(True)
    """

    def __init__(self, set_qasm=False):
        self.set_qasm = set_qasm

    def plot_graph(self, array, label=None):
        """ Draw a graph of data used in quantum clustering algorithm

        Args:
            array (array or list):
                A array of data used in quantum clustering algorithm.
            label (array or list):
                A list of labels for data after clustering. Defaults to None.

        Returns:
            matplotlib.figure:
                A matplotlib figure object of a graph of data used in quantum
                clustering algorithm.

        Example:
            >>> import renom_q.ml.qclustering
            >>> qcl = renom_q.ml.qclustering.QClustering()
            >>> data = [[5, 4], [6, 6], [4, 9], [8, 1]]
            >>> qcl.plot_graph(data)
        """
        array_data = np.array(array).T

        bn = array_data.shape[1]
        plt.xlabel("x")
        plt.ylabel("y")
        plt.xlim([sorted(array_data[0])[0]-1, sorted(array_data[0])[-1]+1])
        plt.ylim([sorted(array_data[1])[0]-1, sorted(array_data[1])[-1]+1])

        for i in range(bn):
            for j in range(bn):
                if i < j:
                    plt.plot([array_data[0][i], array_data[0][j]],
                             [array_data[1][i], array_data[1][j]], 'k-')

        if type(label) is list:
            for i in range(bn):
                if label[i] == 1:
                    plt.plot(array_data[0][i], array_data[1][i], "ro", markersize=20)
                else:
                    plt.plot(array_data[0][i], array_data[1][i], "co", markersize=20)
        else:
            plt.plot(array_data[0], array_data[1], "ro", markersize=20)

        if type(label) is list:
            a_num, b_num, xa, xb, ya, yb = 0, 0, 0, 0, 0, 0

            for i in range(bn):
                if label[i] == 1:
                    xa += array_data[0][i]
                    ya += array_data[1][i]
                    a_num += 1
                else:
                    xb += array_data[0][i]
                    yb += array_data[1][i]
                    b_num += 1
            xa /= a_num
            ya /= a_num
            xb /= b_num
            yb /= b_num

            a = -(xa-xb)/(ya-yb)
            b = (ya+yb)/2-a*(xa+xb)/2
            line = a*array_data[0] + b

            plt.plot(array_data[0], line, ls=':')

        plt.show()

    def qclustering(self, array, mode='euclidean'):
        """ Cluster input data into two classes

        Args:
            array (array or list):
                A array of input data used in quantum clustering algorithm.
            mode (str):
                A　name of distance between each data point. Defaults to 'euclidean'.

        Returns:
            label (array or list):
                A list of labels for data after clustering.

        Example:
            >>> import renom_q.ml.qclustering
            >>> qcl = renom_q.ml.qclustering.QClustering()
            >>> data = [[5, 4], [6, 6], [4, 9], [8, 1]]
            >>> qcl.qclustering(data, mode='mahalanobis')
            Mahalanobis' Distance
            [1, -1, -1, 1]
        """
        if mode == 'mahalanobis':
            print("Mahalanobis' Distance")
        else:
            print("Euclidean distance")

        A = np.array(array).T
        bn = A.shape[1]
        J = np.zeros((bn, bn))
        VI = np.linalg.inv(np.cov(A))
        for i in range(bn):
            for j in range(bn):
                if i < j:
                    u = A[:, i]
                    v = A[:, j]

                    if mode == 'mahalanobis':
                        J[j][i] = J[i][j] = scipy.spatial.distance.mahalanobis(u, v, VI)
                    else:
                        J[j][i] = J[i][j] = scipy.spatial.distance.euclidean(u, v)

        self.result = self.qaa(J, hx=1, maxcut_mode=True, set_qasm=self.set_qasm)

        label = 2*self.result['solution']-1
        label = list(label)

        return label
