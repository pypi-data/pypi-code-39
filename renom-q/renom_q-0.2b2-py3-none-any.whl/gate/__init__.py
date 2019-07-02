# -*- coding: utf-8 -*-

# Copyright 2019, Grid.
#
# This source code is licensed under the ReNom Subscription Agreement, version 1.0.
# ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)


from renom_q.quantumcircuit import QuantumCircuit

from .measure import measure
QuantumCircuit.measure = measure

from .barrier import barrier
QuantumCircuit.barrier = barrier

from .gate_base1 import gate_base1
QuantumCircuit.gate_base1 = gate_base1

from .reset import reset
QuantumCircuit.reset = reset

from .id import id
QuantumCircuit.id = id

from .x import x
QuantumCircuit.x = x

from .y import y
QuantumCircuit.y = y

from .z import z
QuantumCircuit.z = z

from .h import h
QuantumCircuit.h = h

from .s import s
QuantumCircuit.s = s

from .sdg import sdg
QuantumCircuit.sdg = sdg

from .t import t
QuantumCircuit.t = t

from .tdg import tdg
QuantumCircuit.tdg = tdg

from .rx import rx
QuantumCircuit.rx = rx

from .ry import ry
QuantumCircuit.ry = ry

from .rz import rz
QuantumCircuit.rz = rz

from .u1 import u1
QuantumCircuit.u1 = u1

from .u2 import u2
QuantumCircuit.u2 = u2

from .u3 import u3
QuantumCircuit.u3 = u3

from .gate_base2 import gate_base2
QuantumCircuit.gate_base2 = gate_base2

from .cx import cx
QuantumCircuit.cx = cx

from .cy import cy
QuantumCircuit.cy = cy

from .cz import cz
QuantumCircuit.cz = cz

from .ch import ch
QuantumCircuit.ch = ch

from .cs import cs
QuantumCircuit.cs = cs

from .cu1 import cu1
QuantumCircuit.cu1 = cu1

from .cu3 import cu3
QuantumCircuit.cu3 = cu3

from .crz import crz
QuantumCircuit.crz = crz

from .swap import swap
QuantumCircuit.swap = swap

from .ccx import ccx
QuantumCircuit.ccx = ccx

from .cswap import cswap
QuantumCircuit.cswap = cswap
