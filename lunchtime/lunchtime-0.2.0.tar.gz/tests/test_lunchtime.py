#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import pytest
from click.testing import CliRunner
from lunchtime.functions import _crazy_out, clear_term
from lunchtime import cli


def test_cli_help():
    """Test the CLI help."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["--help"])
    assert result.exit_code == 0
    assert "Show this message and exit." in result.output


def test_crazy_out():
    """Test the _crazy_out() function."""
    expect = 14
    result = _crazy_out("testing")
    assert len(result) == expect
