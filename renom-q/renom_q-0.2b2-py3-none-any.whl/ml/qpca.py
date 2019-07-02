# -*- coding: utf-8 -*-

# Copyright 2019, Grid.
#
# This source code is licensed under the ReNom Subscription Agreement, version 1.0.
# ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)


import numpy as np
import math
from scipy.optimize import minimize

from renom_q.quantumregister import QuantumRegister
from renom_q.classicalregister import ClassicalRegister
from renom_q.quantumcircuit import QuantumCircuit
from renom_q.exception import ReNomQError


class QPCA:
    """ Quantum Principle Component Analysis

    Args:
        n_components (int):
            A number of principal components to calculate by quantum PCA algorithm.
            Defaults to None.

    Example:
        >>> import renom_q.ml.qpca
        >>> qpca = renom_q.ml.qpca.QPCA(2)
    """

    def __init__(self, n_components=None):
        self.n_components = n_components
        self.matrix = None
        self.components_ = None

    def vqe_circuit(self, theta, qubit_number, depth):
        """ The circuit using quantum PCA algorithm """
        bn = qubit_number
        q = QuantumRegister(bn)
        c = ClassicalRegister(bn)
        qc = QuantumCircuit(q, c)

        if bn == 1:
            qc.ry(theta[0], q[0])

        else:
            for i in range(depth):
                qc.cx(q[0], q[bn-1])
                for j in range(bn):
                    qc.ry(theta[j], q[j])

        return qc.Qr.qubit

    def get_covariance(self):
        """ Calculate the covariance matrix of the input matrix used in principal component analysis

        Returns:
            cov (array):
                A array of the covariance matrix of the input matrix used in principal
                component analysis.

        Example:
            >>> import renom_q.ml.qpca
            >>> qpca = renom_q.ml.qpca.QPCA(2)
            >>> matrix = [[0.5, 0.8], [0.8, 0.5]]
            >>> qpca.fit(matrix, method='Nelder-Mead')
            >>> qpca.get_covariance()
            array([[ 0.045, -0.045],
                   [-0.045,  0.045]])
        """
        if self.matrix is None:
            raise ReNomQError("this function is only available after using the ",
                              "QPCA.fit() function")

        z = (self.matrix - self.mean_).T
        cov = np.cov(z)

        return cov

    def transform(self, matrix):
        """ Calculate inner product of input matrix and its principal component vector

        Args:
            matrix (list):
                The input matrix used in principal component analysis.

        Returns:
            vec (array):
                A array of inner product of input matrix and its principal component vector.

        Example:
            >>> import renom_q.ml.qpca
            >>> qpca = renom_q.ml.qpca.QPCA(2)
            >>> matrix = [[0.5, 0.8], [0.8, 0.5]]
            >>> qpca.fit(matrix, method='Nelder-Mead')
            >>> qpca.transform(matrix)
            array([[ 0.21213203, -0.15      ],
                   [-0.21213203,  0.15      ]])
        """
        if self.components_ is None:
            raise ReNomQError("this function is only available after using the ",
                              "QPCA.fit() function")

        matrix = np.array(matrix)
        mean = np.mean(matrix, axis=0)
        z = (matrix - mean)

        vec = np.zeros((z.shape[0], self.n_components))
        for i in range(z.shape[0]):
            for j in range(self.n_components):
                vec[i][j] = np.dot(self.components_[j], z[i])

        return vec

    def fit(self, matrix, depth=None, method='Nelder-Mead', n_particle=100, steps=50):
        """ Perform principal component analysis of data

        Args:
            matrix (array or list):
                A matrix to perform principal component analysis.
            depth (boolean):
                A number of circuit depths used in the quantum PCA algorithm.
                Defaults to None.
            method (str):
                A name of optimization algorithm used in quantum PCA algorithm.
                Available method is Nelder-Mead and QPSO. Defaults to 'Nelder-Mead'.
            n_particle (int):
                A number of particles using QPSO method. Defaults to 100.
            steps (int):
                A number of optimal solution searches. Defaults to 50.

        Example:
            >>> import renom_q.ml.qpca
            >>> qpca = renom_q.ml.qpca.QPCA(2)
            >>> matrix = [[0.5, 0.8], [0.8, 0.5]]
            >>> qpca.fit(matrix, method='QPSO', 80, 20)
        """
        self.matrix = np.array(matrix)
        if self.matrix.shape[0] != self.matrix.shape[1]:
            raise ReNomQError("shape (%s," % self.matrix.shape[0],
                              "%s)" % self.matrix.shape[1], " of input martix is not square")
        qubit = np.log2(self.matrix.shape[0])
        if qubit != int(qubit):
            raise ReNomQError("shape (%s," % self.matrix.shape[0],
                              "%s)" % self.matrix.shape[1],
                              " of input martix is not the qubit state number \'2**(qubit number)\'")
        self.mean_ = np.mean(self.matrix, axis=0)

        H = []
        eigenvectors = []
        eigenvalues = []

        H.append(self.get_covariance())

        bn = int(np.log2(H[0].shape[0]))
        depth = bn if depth is None else depth
        num = self.matrix.shape[0] if self.n_components is None else self.n_components

        for step in range(num):
            if step != 0:
                H.append(H[step-1] - np.dot(H[0],
                                            np.outer(eigenvectors[step-1].real, eigenvectors[step-1].real)))

            def expectation(theta):
                Hamiltonian = H[step].copy()
                Hamiltonian *= -1

                vector = self.vqe_circuit(theta, bn, depth)

                e = 0
                for i in range(2**bn):
                    a = vector[i].real
                    for j in range(2**bn):
                        b = vector[j].real
                        e += Hamiltonian[i][j]*a*b

                return e

            if method == 'QPSO':
                """ Quantum Particle Swarm Optimization (QPSO) method """
                particles = []
                x_begin = y_begin = 0
                x_end = y_end = 2*np.pi
                best_value = 9999
                best_position = np.array(num)
                g = 1.7

                for i in range(n_particle):
                    particles.append(self.QPSO(2 * x_end * np.random.random(bn) - x_end))

                for i in range(steps):
                    values = []

                    for particle in particles:
                        particle.get_value(expectation)
                        values.append(particle.value)

                    for particle in particles:
                        if particle.value < best_value:
                            best_value = particle.value
                            best_position = particle.position

                        particle.update(best_position, g)

                theta = best_position.copy()
                eigenvalues.append(-best_value)
                eigenvectors.append(self.vqe_circuit(theta, bn, depth).real.copy())

            else:
                """ Nelder-Mead method """
                initial_params = []
                for i in range(bn):
                    initial_params.append(np.random.uniform(0.0, 2*np.pi))

                result_list = []
                eval_list = []
                for i in range(steps):
                    minimum = minimize(expectation, initial_params,
                                       method='Nelder-Mead', options={'xatol': 1.0e-4})
                    result_list.append(minimum.x)
                    eval_list.append(expectation(minimum.x))

                eigenvalue = sorted(eval_list)[0]
                idx = eval_list.index(eigenvalue)
                theta = result_list[idx]
                eigenvalues.append(-eigenvalue)
                eigenvectors.append(self.vqe_circuit(theta, bn, depth).real.copy())

        self.eigenvalue = eigenvalues
        self.components_ = np.array(eigenvectors)

    class QPSO:
        """ Quantum Particle Swarm Optimization (QPSO) method """

        def __init__(self, x):
            self.position = x
            self.best_value = 9999
            self.best_position = self.position
            self.value = 0

        def get_value(self, fun):
            value = fun(self.position)
            if value < self.best_value:
                self.best_value = value
                self.best_position = self.position
            self.value = value

        def update(self, best_position, g, potential='delta'):
            phi = np.random.random(2)

            P = (phi[0] * self.best_position + phi[1] * best_position)/(phi[0]+phi[1])

            u = np.random.random(1)
            up = 0
            if potential == 'delta':
                up = 1/(2*g*math.log(2**0.5)) * abs(self.position - P)
            elif potential == 'harmonic':
                up = 1 / (0.47694*g) * (log(1/u))**0.5 * abs(self.position - P)

            if np.random.random(1) > 0.5:
                self.position = P + up
            else:
                self.position = P - up
