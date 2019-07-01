# Copyright 2016 IBM Corp.
# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

r"""
=============================================
B112: Test for a continue in the except block
=============================================

Errors in Python code bases are typically communicated using ``Exceptions``.
An exception object is 'raised' in the event of an error and can be 'caught' at
a later point in the program, typically some error handling or logging action
will then be performed.

However, it is possible to catch an exception and silently ignore it while in
a loop. This is illustrated with the following example

.. code-block:: python

    while keep_going:
      try:
        do_some_stuff()
      except Exception:
        continue

This pattern is considered bad practice in general, but also represents a
potential security issue. A larger than normal volume of errors from a service
can indicate an attempt is being made to disrupt or interfere with it. Thus
errors should, at the very least, be logged.

There are rare situations where it is desirable to suppress errors, but this is
typically done with specific exception types, rather than the base Exception
class (or no type). To accommodate this, the test may be configured to ignore
'try, except, continue' where the exception is typed. For example, the
following would not generate a warning if the configuration option
``checked_typed_exception`` is set to False:

.. code-block:: python

    while keep_going:
      try:
        do_some_stuff()
      except ZeroDivisionError:
        continue

**Config Options:**

.. code-block:: yaml

    try_except_continue:
      check_typed_exception: True


:Example:

.. code-block:: none

    >> Issue: Try, Except, Continue detected.
       Severity: Low   Confidence: High
       Location: ./examples/try_except_continue.py:5
    4            a = i
    5        except:
    6            continue

.. seealso::

 - https://security.openstack.org

.. versionadded:: 1.0.0

"""

import ast

import bandit
from bandit.core import test_properties as test


def gen_config(name):
    if name == 'try_except_continue':
        return {'check_typed_exception': False}


@test.takes_config
@test.checks('ExceptHandler')
@test.test_id('B112')
def try_except_continue(context, config):
    node = context.node
    if len(node.body) == 1:
        if (not config['check_typed_exception'] and
                node.type is not None and
                getattr(node.type, 'id', None) != 'Exception'):
            return

        if isinstance(node.body[0], ast.Continue):
            return bandit.Issue(
                severity=bandit.LOW,
                confidence=bandit.HIGH,
                text=("Try, Except, Continue detected."))
