# -*- coding: utf-8 -*-
"""
Test suite for :module:`unittest_resources`. Not part of the public API.

More details on project `README.md` and
`repository <https://gitlab.com/ergoithz/unittest-resources/>`_.

License
-------
MIT (see LICENSE file).
"""

import unittest_resources
import unittest_resources.testing as bases


class TypingTestCase(bases.TypingTestCase):
    """TestCase checking :module:`mypy`."""

    meta_module = unittest_resources.__name__


class CodeStyleTestCase(bases.CodeStyleTestCase):
    """TestCase checking :module:`pycodestyle`."""

    meta_module = unittest_resources.__name__


class DocStyleTestCase(bases.DocStyleTestCase):
    """TestCase checking :module:`pydocstyle`."""

    meta_resources = [
        (unittest_resources.__name__, '__init__.py'),
        (unittest_resources.__name__, 'testing.py'),
        ]


class MaintainabilityIndexTestCase(bases.MaintainabilityIndexTestCase):
    """TestCase checking :module:`radon` maintainability index."""

    meta_module = unittest_resources.__name__


class CodeComplexityTestCase(bases.CodeComplexityTestCase):
    """TestCase checking :module:`radon` code complexity."""

    meta_module = unittest_resources.__name__
    max_class_complexity = 8
    max_function_complexity = 6
