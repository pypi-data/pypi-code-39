#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner

from yeahyeah import cli
from yeahyeah.core import YeahYeah
from plugins.url_patterns import UrlPatternsPlugin


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.yeahyeah)
    assert result.exit_code == 0


def test_plugin(url_pattern_list, mock_web_browser):
    yeahyeah = YeahYeah()
    plugin = UrlPatternsPlugin(pattern_list=url_pattern_list)
    yeahyeah.add_plugin(plugin)

    runner = CliRunner()
    assert (
        runner.invoke(yeahyeah.root_cli, ["test1", "val1", "val2"]).output
        == "https://hostval1/somethingval2.php\n"
    )
