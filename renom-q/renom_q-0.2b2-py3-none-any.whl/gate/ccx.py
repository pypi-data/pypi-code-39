# -*- coding: utf-8 -*-

# Copyright 2019, Grid.
#
# This source code is licensed under the ReNom Subscription Agreement, version 1.0.
# ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)


import numpy as np

from renom_q.quantumcircuit import QuantumCircuit


def ccx(self, q_ctl1, q_ctl2, q_tgt):
    """ Apply ccx gate to quantum register.

    Args:
        q_ctl1 (tuple):
            A tuple of a quantum register and its index (ex:q[0]). It's one
            of the control qubit.
        q_ctl2 (tuple):
            A tuple of a quantum register and its index (ex:q[0]). It's one
            of the control qubit.
        q_tgt (tuple):
            A tuple of a quantum register and its index (ex:q[0]). It's the
            target qubit.

    Example:
        >>> import renom_q
        >>> q = renom_q.QuantumRegister(3)
        >>> c = renom_q.ClassicalRegister(3)
        >>> qc = renom_q.QuantumCircuit(q, c)
        >>> qc.ccx(q[0], q[1], q[2])
    """
    name_ctl1, origin_ctl1 = q_ctl1
    name_ctl1, ctl1 = self.convert_q_number(q_ctl1)
    name_ctl2, origin_ctl2 = q_ctl2
    name_ctl2, ctl2 = self.convert_q_number(q_ctl2)
    name_tgt, origin_tgt = q_tgt
    name_tgt, tgt = self.convert_q_number(q_tgt)
    xgate = np.array([[0., 1.], [1., 0.]])
    gate = np.zeros((self.Qr.q_states, self.Qr.q_states), dtype=complex)
    for i in range(self.Qr.q_states):
        bit_c1 = int(int(format(i, 'b')) / 10**(self.Qr.num - ctl1 - 1) % 2)
        bit_c2 = int(int(format(i, 'b')) / 10**(self.Qr.num - ctl2 - 1) % 2)
        if bit_c1 == 1 and bit_c2 == 1:
            bit_t = int(int(format(i, 'b')) / 10**(self.Qr.num - tgt - 1) % 2)
            bit_list = list(format(i, '0' + str(self.Qr.num) + 'b'))
            bit_list[tgt] = '1' if bit_t == 0 else '0'
            idx = int("".join(bit_list), 2)
            if i < idx:
                gate[i, i] = xgate[bit_t, 0]
                gate[i, idx] = xgate[bit_t, 1]
            else:
                gate[i, i] = xgate[bit_t, 1]
                gate[i, idx] = xgate[bit_t, 0]
        else:
            gate[i, i] = 1.
    qubit = self.Qr.qubit
    self.Qr.qubit = np.dot(gate, self.Qr.qubit)

    if self.print_matrix_bool:
        self.matrixlist.append('\n---------------- ccx(' + name_ctl1 + '[' + str(origin_ctl1)
                               + '], ' + name_ctl2 +
                               '[' + str(origin_ctl2) + '], ' + name_tgt +
                               '[' + str(origin_tgt) + ']) ----------------\n'
                               + str(gate) + '・\n\n' + str(np.array(qubit).reshape(self.Qr.q_states, 1)) +
                               ' = \n\n' + str(np.array(self.Qr.qubit).reshape(self.Qr.q_states, 1)))
        tensor = '\n---------------- ccX ----------------\n' + str(gate)
        self.tensorlist.append(tensor)

    if self.qasm_bool:
        self.qasmlist.append('ccx ' + name_ctl1 + '[' + str(origin_ctl1) + '], '
                             + name_ctl2 + '[' + str(origin_ctl2) + '], ' + name_tgt + '[' + str(origin_tgt) + '];')

    return self
