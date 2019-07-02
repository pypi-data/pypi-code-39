# -*- coding: utf-8 -*-

# Copyright 2019, Grid.
#
# This source code is licensed under the ReNom Subscription Agreement, version 1.0.
# ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)


from random import random
import numpy as np
import matplotlib.pyplot as plt

from renom_q.exception import ReNomQError
from .qaa import QAA


class QAE(QAA):
    """ Quantum AutoEncoder

    Args:
        set_qasm (boolean):
            If it is true, qasm code is added to the calculation result.
            Defaults to False.

    Example:
        >>> import renom_q.ml.qae
        >>> qae = renom_q.ml.qae.QAE(True)
    """

    def __init__(self, set_qasm=False):
        self.convolution = False
        self.set_qasm = set_qasm

    def ising(self, matrix):
        """ Convert qubit state to spin state of ising model
        [0, 1, 0, 1] => [-1, 1, -1, 1]

        Args:
            matrix (array or list):
                A list of the each qubit state. A qubit has two states of 0 and 1.

        Returns:
            (array):
                A list of the each spin state of ising model. The state of up
                spin is expressed as 1 and The state of down spin is expressed as -1.

        Example:
            >>> import renom_q.ml.qae
            >>> qae = renom_q.ml.qae.QAE()
            >>> spin = [0, 1, 0, 1, 0]
            >>> qae.ising(spin)
            array([-1,  1, -1,  1, -1])
        """
        return 2*np.array(matrix)-1

    def qubo(self, matrix):
        """ Convert spin state of ising model to qubit state
        [-1, 1, -1, 1] => [0, 1, 0, 1]

        Args:
            matrix (array or list):
                A list of the each spin state of ising model. The state of up
                spin is expressed as 1 and The state of down spin is expressed as -1.

        Returns:
            (array):
                A list of the each qubit state. A qubit has two states of 0 and 1.

        Example:
            >>> import renom_q.ml.qae
            >>> qae = renom_q.ml.qae.QAE()
            >>> spin = [-1, 1, -1, 1, -1]
            >>> qae.qubo(spin)
            array([0., 1., 0., 1., 0.])
        """
        return (np.array(matrix)+1)*0.5

    def draw_image(self, spin_list, grid=True):
        """ Draw an image in a quantum autoencoder algorithm

        Args:
            spin_list (list):
                A list of the each spin state of ising model. The state of up
                spin is expressed as 1 and The state of down spin is expressed as -1.
            grid (boolean):
                If it is true, add grid lines to the drawing image. Defaults to True.

        Returns:
            matplotlib.figure:
                A matplotlib figure object of an image in a quantum autoencoder algorithm.

        Example:
            >>> import renom_q.ml.qae
            >>> qae = renom_q.ml.qae.QAE()
            >>> ising = [-1, 1, -1, -1, 1, -1, -1, 1, -1]
            >>> qae.draw_image(ising)
        """
        spin = np.array(spin_list)
        bn = spin.shape[0]

        nd = spin.reshape(int(np.sqrt(bn)), int(np.sqrt(bn)))
        plt.xticks(color="None")
        plt.yticks(color="None")
        plt.tick_params(length=0)
        plt.xticks([(i-0.5) for i in range(int(np.sqrt(bn))+1)])
        plt.yticks([(i-0.5) for i in range(int(np.sqrt(bn))+1)])
        if grid:
            plt.grid()
        plt.imshow(nd, cmap='gray', vmin=-1, vmax=1)
        plt.show()

    def original(self, number=3, mark=[]):
        """ Setting a original image using quantum autoencoder algorithm

        Args:
            number (int or list or array):
                If 'number' type is int or float, the image is a square whose side is the
                number specified by 'number'. The minimum size is 3x3 images.
                If 'number' type is list or array (matrix), the image is visualized
                by scalar data of matrix 'number'. Defaults to 3.
            mark (list or array):
                A list specifying the grid numbers to make the color black. Specify
                either one-dimensional array or two-dimensional array. Defaults to
                empty list.

        Example:
            >>> import renom_q.ml.qae
            >>> qae = renom_q.ml.qae.QAE()
            >>> qae.original(4, [1, 5, 15])
        """
        if type(number) is int:
            if number <= 2:
                raise ReNomQError("the minimum size is 3 * 3 images")
            if number > 3:
                self.convolution = True
            self.bn = number**2

            cbit = [1 for i in range(self.bn)]
            for i in range(len(mark)):
                if type(mark[i]) is int:
                    cbit[mark[i]] = 0
                elif type(mark[i]) is list:
                    idx = mark[i][0]*number+mark[i][1]
                    cbit[idx] = 0

        elif type(number) is np.ndarray or type(number) is list:
            number = np.array(number)
            if number.shape[0] <= 2 or number.shape[1] <= 2:
                raise ReNomQError("the minimum size is 3 * 3 images")
            if number.shape[0] != number.shape[1]:
                raise ReNomQError("shape (%s," % number.shape[0],
                                  "%s)" % number.shape[1], " is not square")
            if number.shape[0] > 3:
                self.convolution = True
            self.bn = number.shape[0]**2
            cbit = number.reshape(1, self.bn)[0]

        self.original_state = self.ising(cbit)

    def add_noise(self, noise_rate=0.1):
        """ Add noise the original image

        Args:
            noise_rate (float):
                A number of percentages of noise to be mixed into the original image.
                This can be specified from 0 to 1. Defaults to 0.1.

        Example:
            >>> import renom_q.ml.qae
            >>> qae = renom_q.ml.qae.QAE()
            >>> qae.original(4, [1, 5, 15])
            >>> qae.add_noise(0.3)
        """
        if self.convolution:
            J = np.array([[0 for column in range(self.bn)] for row in range(self.bn)])
            for i in range(self.bn):
                for j in range(self.bn):
                    J[i][j] = self.original_state[i]*self.original_state[j]*(-1)
            self.J = J
        else:
            J = np.array([[0 for column in range(self.bn)] for row in range(self.bn)])
            for i in range(self.bn):
                Nx = np.sqrt(self.bn)
                Ny = np.sqrt(self.bn)
                a = i//Ny
                b = i % Ny
                n1 = int(Ny*((a-1) % Nx) + b)
                n2 = int(Ny*a + (b-1) % Ny)
                n3 = int(Ny*a + (b+1) % Ny)
                n4 = int(Ny*((a+1) % Nx) + b)
                J[i][n1] = self.original_state[i]*self.original_state[n1]*(-1)
                J[i][n2] = self.original_state[i]*self.original_state[n2]*(-1)
                J[i][n3] = self.original_state[i]*self.original_state[n3]*(-1)
                J[i][n4] = self.original_state[i]*self.original_state[n4]*(-1)
            self.J = J

        for i in range(self.bn):
            for j in range(i+1, self.bn):
                if self.original_state[i] == self.original_state[j] == 1:
                    n = random()
                    if n < noise_rate:
                        self.J[i][j] *= -1
                        self.J[j][i] *= -1

        image = self.original_state.copy()
        noise_rate_dict = {}
        for i in range(self.bn):
            Nx = np.sqrt(self.bn)
            Ny = np.sqrt(self.bn)
            a = i//Ny
            b = i % Ny
            n1 = int(Ny*((a-1) % Nx) + b)
            n2 = int(Ny*a + (b-1) % Ny)
            n3 = int(Ny*a + (b+1) % Ny)
            n4 = int(Ny*((a+1) % Nx) + b)
            p = 1 if self.J[i][n1]/self.original_state[n1] == self.original_state[i] else 0
            p += 1 if self.J[i][n2]/self.original_state[n2] == self.original_state[i] else 0
            p += 1 if self.J[i][n3]/self.original_state[n3] == self.original_state[i] else 0
            p += 1 if self.J[i][n4]/self.original_state[n4] == self.original_state[i] else 0
            p /= 4
            noise_rate_dict['q'+str(i)] = p
            if p >= 0.5:
                p = 1.0
            else:
                p = 0.0
            if random() < p:
                image[i] *= -1

        self.noise_rate_dict = noise_rate_dict
        self.noise_state = image

        if self.convolution:
            number_list = np.zeros((self.bn, 9), dtype='int')
            for i in range(self.bn):
                number_list[i][4] = i
                Nx = np.sqrt(self.bn)
                Ny = np.sqrt(self.bn)
                a = i//Ny
                b = i % Ny
                number_list[i][1] = int(Ny*((a-1) % Nx) + b)
                number_list[i][3] = int(Ny*a + (b-1) % Ny)
                number_list[i][5] = int(Ny*a + (b+1) % Ny)
                number_list[i][7] = int(Ny*((a+1) % Nx) + b)
                c = (a-1) % Ny
                d = (a+1) % Ny
                number_list[i][0] = int(Ny*c + (b-1) % Ny)
                number_list[i][2] = int(Ny*c + (b+1) % Ny)
                number_list[i][6] = int(Ny*d + (b-1) % Ny)
                number_list[i][8] = int(Ny*d + (b+1) % Ny)
            self.number_list = number_list

            all_hz = np.zeros((self.bn, 9), dtype='int')
            for i in range(self.bn):
                for j in range(9):
                    all_hz[i][j] = -self.original_state[number_list[i][j]]
            self.hz = all_hz
        else:
            self.hz = -self.original_state

    def decode(self, plot_filter=False):
        """ Add noise the original image

        Args:
            plot_filter (boolean):
                If it is true, the denoised image at each filter in the convolutional
                quantum self-coder is drawn. This can only be specified for images
                larger than 3x3. Defaults to False.

        Example:
            >>> import renom_q.ml.qae
            >>> qae = renom_q.ml.qae.QAE()
            >>> qae.original(4, [1, 5, 15])
            >>> qae.add_noise(0.3)
            >>> qae.decode(True)
        """
        if self.convolution:
            final_image = np.array([0 for i in range(self.bn)])
            result_list = {}

            for i in range(self.bn):
                result = self.qaa(self.J, self.hz[i], hx=1, ae_mode=True,
                                  convolution=self.convolution, cqae_list=self.number_list, cqae_spin=i, set_qasm=self.set_qasm)
                result_list[str(i)] = result

                if plot_filter:
                    print(i)
                    self.draw_image(self.ising(result['solution']))
                final_image[i] = result['solution'][4]

            self.decoded_state = self.ising(final_image)
            result_list['noise rate'] = self.noise_rate_dict
            self.result = result_list

        else:
            result = self.qaa(self.J, self.hz, hx=1, ae_mode=True, set_qasm=self.set_qasm)
            self.decoded_state = self.ising(result['solution'])
            result['noise rate'] = self.noise_rate_dict
            self.result = result
