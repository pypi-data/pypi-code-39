# -*- coding: utf-8 -*-

# Copyright 2019, Grid.
#
# This source code is licensed under the ReNom Subscription Agreement, version 1.0.
# ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)


import numpy as np
import math

from renom_q.quantumregister import QuantumRegister
from renom_q.classicalregister import ClassicalRegister
from renom_q.quantumcircuit import QuantumCircuit
from renom_q.utilitys import execute
from renom_q.exception import ReNomQError


class QAA:
    """ Quantum Adiabatic Algorithm """

    def rx(self, qci, theta, q):
        """ rx gate   { Exp**(j * theta * X) } """
        qci.u3(theta, -math.pi/2, math.pi/2, q)

    def rz(self, qci, phi, q):
        """ rz gate   { Exp**(j * theta * Z) } """
        qci.u1(phi, q)

    def rzz(self, qci, phi, q1, q2):
        """ rzz gate   { Exp**(j * theta * ZZ) } """
        qci.cx(q1, q2)
        self.rz(qci, -2.0*phi, q2)
        qci.cx(q1, q2)

    def qaa(self, J, hz=None, hx=-1.0, tm=10, dt=0.1, shots=1024, maxcut_mode=False,
            ae_mode=False, convolution=False, cqae_list=None, cqae_spin=None, set_qasm=False):
        """ The optimization algorithm by quantum adiabatic calcutation

        Args:
            J (int, float, array or list): 
                A Matrix of coupling coefficients applied to spins of Ising model.
            hz (list):
                A List of longitudinal magnetic field coefficients applied to
                each spin of Ising model. Defaults to None.
            hx (int or float):
                A transverse field coefficient uniformly applied to spins of Ising model.
                Defaults to -1.0.
            tm (int or float):
                A evolution time in the Hamiltonian Schrodinger equation of Ising model.
                The number of steps in QAA is tm/dt. Defaults to 10.
            dt (int or float):
                A time interval of time evolution in the Hamiltonian Schrodinger
                equation of the Ising model. The number of steps in QAA is tm/dt.
                Defaults to 0.1.
            shots (int):
                The number of excutions of quantum circuit mesurement. Defaults to
                1024.
            maxcut_mode (boolean):
                If it is True, the sign of J is inverted during calculation.
                Defaults to False.
            ae_mode (boolean):
                If it is true, each spin in the Ising model is affected only by
                the 4 adjacent spins. Defaults to False.
            convolution (boolean):
                If it is true, it is calculated with a convolution filter composed
                of 9 qubits in the quantum autoencoder algorithm. Defaults to False.
            cqae_list (list):
                A list to use when boolean convolution is True. Defaults to None.
            cqae_spin (int):
                A number of qubit to use when boolean convolution is True. Defaults to None.
            set_qasm (boolean):
                If it is true, qasm code is added to the calculation result.
                Defaults to False.

        Returns:
            result (dict):
                A dict of the calculation result and each parameter of adiabatic
                quantum calculation.

        Example:
            >>> import renom_q.ml.qaa
            >>> qaa = renom_q.ml.qaa.QAA()
            >>> J = -1
            >>> hz = [-1, 1]
            >>> qaa.qaa(J, hz)
            {'solution': array([0, 1]), 'result': {'00': 280, '01': 510, '11': 234},
            'J': -1, 'hz': [-1, 1], 'hx': -1.0, 'shots': 1024, 'qasm': None}
        """
        if convolution:
            bn = 9
        elif type(J) is int or type(J) is float:
            bn = 2
        else:
            J = np.array(J)
            if J.shape[0] != J.shape[1]:
                raise ReNomQError("shape (%s," % J.shape[0],
                                  "%s)" % J.shape[1], " of J is not square")
            bn = int(J.shape[0])

        if maxcut_mode:
            hx = 1

        rz_mode = False
        if hz is not None:
            if not convolution and bn != np.array(hz).shape[0]:
                raise ReNomQError("shape of J and length of hz is mismatch")
            rz_mode = True

        q = QuantumRegister(bn)
        c = ClassicalRegister(bn)
        qc = QuantumCircuit(q, c, set_qasm=set_qasm)

        for i in range(bn):
            qc.h(q[i])
        step = math.floor(tm/dt)

        if ae_mode:
            nx = np.sqrt(bn)
            ny = np.sqrt(bn)
        for i in range(0, step):
            s = i / step
            for j in range(bn):
                self.rx(qc, -2.0*(1-s)*hx*dt, q[j])
                if rz_mode:
                    self.rz(qc, -2.0*s*hz[j]*dt, q[j])
                if ae_mode:
                    a = j//ny
                    b = j % ny
                    n1 = int(ny*((a-1) % nx) + b)
                    n2 = int(ny*a + (b-1) % ny)
                    n3 = int(ny*a + (b+1) % ny)
                    n4 = int(ny*((a+1) % nx) + b)
                for k in range(j+1, bn):
                    if bn == 2:
                        self.rzz(qc, s*J*dt, q[j], q[k])
                    elif ae_mode:
                        if k == n1 or k == n2 or k == n3 or k == n4:
                            if convolution:
                                row = cqae_list[cqae_spin][j]
                                column = cqae_list[cqae_spin][k]
                                self.rzz(qc, -s*J[row][column]*dt, q[j], q[k])
                            else:
                                self.rzz(qc, -s*J[j][k]*dt, q[j], q[k])
                    else:
                        if maxcut_mode:
                            self.rzz(qc, -s*J[j][k]*dt, q[j], q[k])
                        else:
                            self.rzz(qc, s*J[j][k]*dt, q[j], q[k])

        qc.measure()

        r = execute(qc, shots)

        solution = sorted(r.items(), key=lambda x: x[1])
        solution = np.array([int(i) for i in solution[-1][0]])
        qasm = qc.qasm() if set_qasm else None

        result = {'solution': solution,
                  'result': r,
                  'J': J,
                  'hz': hz,
                  'hx': hx,
                  'shots': shots,
                  'qasm': qasm}

        return result
