# -*- coding: utf-8 -*-

# Copyright 2019, Grid.
#
# This source code is licensed under the ReNom Subscription Agreement, version 1.0.
# ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)


from renom_q.quantumcircuit import QuantumCircuit


def barrier(self, *args):
    """ Add a barrier block in circuit diagram.

    args:
        *args (renom_q.QuantumRegister, tuple or None):
            If arg type is a tuple (ex: q[0]), a quantum register No.0 is
            added a barrier block. If arg type is a renom_q.QuantumRegister,
            all quantum registers in renom_q.QuantumRegister are added a
            barrier block. If arg type is None, all of multiple quantum
            registers are added a barrier block.

    Example:
        >>> import renom_q
        >>> q = renom_q.QuantumRegister(2)
        >>> c = renom_q.ClassicalRegister(2)
        >>> qc = renom_q.QuantumCircuit(q, c)
        >>> qc.barrier()
    """
    STR = 'barrier '
    if args == ():
        for i in range(self.circuit_number + 1):
            for j in range(self.Qr.numlist[i]):
                name = [k for k, v in self.Qr.dict.items() if v == i][0]
                STR += str(name) + '[' + str(j) + '], '
    elif str(args[0]) in self.Qr.dict:
        for i in args:
            name = i.name
            idx = self.Qr.dict[name]
            for j in range(self.Qr.numlist[idx]):
                STR += str(name) + '[' + str(j) + '], '
    elif type(args[0]) is tuple:
        for i in args:
            name, num = i
            STR += str(name) + '[' + str(num) + '], '

    STR = STR.rstrip(', ')
    STR += ';'
    if self.qasm_bool:
        self.qasmlist.append(STR)

    return self
