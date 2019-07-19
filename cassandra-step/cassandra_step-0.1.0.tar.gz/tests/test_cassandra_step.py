#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cassandra_step` package."""

import pytest  # noqa: F401
import cassandra_step  # noqa: F401


def test_construction():
    """Simplest test that we can make a Cassandra object"""
    cass = cassandra_step.Cassandra()
    assert str(type(cass)) == "<class 'cassandra_step.cassandra.Cassandra'>"
