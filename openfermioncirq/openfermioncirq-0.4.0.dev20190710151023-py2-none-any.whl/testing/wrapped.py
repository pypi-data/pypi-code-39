# coding=utf-8
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import
from typing import Any, Dict, Optional, Sequence, Type, Union

import cirq
import sympy


_setup_code = (u'import cirq\n'
               u'import numpy as np\n'
               u'import sympy\n'
               u'import openfermioncirq as ofc\n'
               u'import openfermion as of\n')


def assert_equivalent_repr(
        value, **_3to2kwargs):
    if 'setup_code' in _3to2kwargs: setup_code = _3to2kwargs['setup_code']; del _3to2kwargs['setup_code']
    else: setup_code =  _setup_code
    u"""Checks that eval(repr(v)) == v.

    Args:
        value: A value whose repr should be evaluatable python
            code that produces an equivalent value.
        setup_code: Code that must be executed before the repr can be evaluated.
            Ideally this should just be a series of 'import' lines.
    """
    cirq.testing.assert_equivalent_repr(value, setup_code=setup_code)


def assert_implements_consistent_protocols(
        val, **_3to2kwargs
        ):
    if 'local_vals' in _3to2kwargs: local_vals = _3to2kwargs['local_vals']; del _3to2kwargs['local_vals']
    else: local_vals =  None
    if 'global_vals' in _3to2kwargs: global_vals = _3to2kwargs['global_vals']; del _3to2kwargs['global_vals']
    else: global_vals =  None
    if 'setup_code' in _3to2kwargs: setup_code = _3to2kwargs['setup_code']; del _3to2kwargs['setup_code']
    else: setup_code =  _setup_code
    if 'ignoring_global_phase' in _3to2kwargs: ignoring_global_phase = _3to2kwargs['ignoring_global_phase']; del _3to2kwargs['ignoring_global_phase']
    else: ignoring_global_phase = False
    if 'qubit_count' in _3to2kwargs: qubit_count = _3to2kwargs['qubit_count']; del _3to2kwargs['qubit_count']
    else: qubit_count =  None
    if 'exponents' in _3to2kwargs: exponents = _3to2kwargs['exponents']; del _3to2kwargs['exponents']
    else: exponents =  (
            0, 1, -1, 0.5, 0.25, -0.5, 0.1, sympy.Symbol(u's'))
    u"""Checks that a value is internally consistent and has a good __repr__."""

    cirq.testing.assert_implements_consistent_protocols(
        val,
        exponents=exponents,
        qubit_count=qubit_count,
        ignoring_global_phase=ignoring_global_phase,
        setup_code=setup_code,
        global_vals=global_vals,
        local_vals=local_vals)


def assert_eigengate_implements_consistent_protocols(
        eigen_gate_type, **_3to2kwargs):
    if 'local_vals' in _3to2kwargs: local_vals = _3to2kwargs['local_vals']; del _3to2kwargs['local_vals']
    else: local_vals =  None
    if 'global_vals' in _3to2kwargs: global_vals = _3to2kwargs['global_vals']; del _3to2kwargs['global_vals']
    else: global_vals =  None
    if 'setup_code' in _3to2kwargs: setup_code = _3to2kwargs['setup_code']; del _3to2kwargs['setup_code']
    else: setup_code =  _setup_code
    if 'ignoring_global_phase' in _3to2kwargs: ignoring_global_phase = _3to2kwargs['ignoring_global_phase']; del _3to2kwargs['ignoring_global_phase']
    else: ignoring_global_phase = False
    if 'qubit_count' in _3to2kwargs: qubit_count = _3to2kwargs['qubit_count']; del _3to2kwargs['qubit_count']
    else: qubit_count =  None
    if 'global_shifts' in _3to2kwargs: global_shifts = _3to2kwargs['global_shifts']; del _3to2kwargs['global_shifts']
    else: global_shifts =  (0, -0.5, 0.1)
    if 'exponents' in _3to2kwargs: exponents = _3to2kwargs['exponents']; del _3to2kwargs['exponents']
    else: exponents =  (
            0, 1, -1, 0.25, -0.5, 0.1, sympy.Symbol(u's'))
    u"""Checks that an EigenGate subclass is internally consistent and has a
    good __repr__."""

    cirq.testing.assert_eigengate_implements_consistent_protocols(
        eigen_gate_type,
        exponents=exponents,
        global_shifts=global_shifts,
        qubit_count=qubit_count,
        ignoring_global_phase=ignoring_global_phase,
        setup_code=setup_code,
        global_vals=global_vals,
        local_vals=local_vals)
