# -*- coding: utf-8 -*-

# Copyright 2019, Grid.
#
# This source code is licensed under the ReNom Subscription Agreement, version 1.0.
# ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)


import numpy as np

from renom_q import *
from renom_q.ml.qae import QAE
from renom_q.ml.qsvm import QSVM
from renom_q.ml.qclustering import QClustering
from renom_q.ml.qpca import QPCA


def test_qae():
    qae = QAE()
    qae.original(3)
    qae.add_noise(0.3)
    qae.decode()
    qae.original(4, [2, 4, 6, 15])
    qae.original(5, [[0, 2], [1, 2], [2, 2], [3, 2], [4, 2]])
    qae.original([[0, 1, 0], [0, 1, 0], [0, 1, 0]])
    r = qae.result
    assert r


def test_qsvm():
    train_xy = np.array([[5, 4], [6, 6]])
    train_label = np.array([1, -1])
    qsvm = QSVM()
    qsvm.fit(train_xy, train_label)
    test_xy = np.array([[3, 3]])
    test_label1 = qsvm.predict(test_xy)

    train_xy = np.array([[5, 4, 2, 1], [6, 6, 7, 3]])
    train_label = np.array([1, -1])
    qsvm.fit(train_xy, train_label)
    test_xy = np.array([[3, 3, 3, 3]])
    test_label2 = qsvm.predict(test_xy)

    assert [test_label1, test_label2]


def test_qcl():
    data_xy = np.array([[5, 4], [6, 6], [3, 3], [2, 1]])

    qcl = QClustering()
    label1 = qcl.qclustering(data_xy, mode='euclidean')
    label2 = qcl.qclustering(data_xy, mode='mahalanobis')

    assert [label1, label2]


def test_qpca():
    mnist_image = np.array([[0., 0., 0., 0.00392157, 0.04313725, 0.,  0., 0.],
                            [0., 0., 0., 0.02745098, 0.03137255, 0.,  0., 0.],
                            [0., 0., 0.00392157, 0.05098039, 0.02352941, 0.00784314,  0.00784314, 0.],
                            [0., 0., 0.02745098, 0.05882353, 0., 0.03529412,  0.03137255, 0.],
                            [0., 0.01960784, 0.0627451,  0.03921569, 0., 0.0627451,  0.02352941, 0.],
                            [0., 0.01568627, 0.05882353, 0.0627451,
                                0.05098039, 0.0627451,  0.00392157, 0.],
                            [0., 0., 0., 0.01176471, 0.05882353, 0.03921569,  0., 0.],
                            [0., 0., 0., 0.00784314, 0.0627451,  0.01568627,  0., 0.]])

    n_components = 2
    qpca = QPCA(n_components=n_components)
    qpca.fit(mnist_image, method='Nelder-Mead', steps=1)
    a = qpca.eigenvalue
    b = qpca.components_
    qpca = QPCA(n_components=n_components)
    qpca.fit(mnist_image, method='QPSO', n_particle=10, steps=10)
    c = qpca.eigenvalue
    d = qpca.components_

    assert [a, b, c, d]
