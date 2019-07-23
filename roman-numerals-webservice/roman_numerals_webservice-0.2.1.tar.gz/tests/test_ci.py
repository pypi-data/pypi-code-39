#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `roman_numerals_webservice` package."""

import pytest

from click.testing import CliRunner

from roman_numerals_webservice import roman_numerals_webservice
from roman_numerals_webservice import cli



def test_command_line_interface():
    """Test the CLI."""

  
    runner = CliRunner()
    result = runner.invoke(cli.main, ['--dry_run=true','--port=8081'])
    assert result.exit_code == 0
    #assert 'roman_numerals_webservice.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
   
    assert "--port INTEGER" in help_result.output
    assert "--host TEXT" in help_result.output
    assert "--port INTEGER" in help_result.output
    assert "--dry_run BOOLEAN" in help_result.output