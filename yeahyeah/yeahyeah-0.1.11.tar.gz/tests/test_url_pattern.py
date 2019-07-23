#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest

from click.testing import CliRunner

from yeahyeah.core import YeahYeahMenuItem
from yeahyeah.plugins.url_patterns import (
    UrlPattern,
    URLPatternList,
    WildCardUrlPattern,
    UrlPatternsPlugin,
)
from tests import RESOURCE_PATH


def test_capture_all(mock_web_browser):
    """You can use {*} as a special key that captures all input parameters in one"""
    pattern_regular = UrlPattern(
        name="test5", pattern="https://{normal}"
    ).to_click_command()
    pattern_with_asterisk = WildCardUrlPattern(
        name="test5", pattern="https://search {query}"
    ).to_click_command()

    runner = CliRunner()
    result = runner.invoke(pattern_with_asterisk, ["one", "two", "three"])
    assert result.output == "loading https://search one two three\n"

    result = runner.invoke(pattern_regular, ["one", "two", "three"])
    assert result.exit_code != 0
    assert "Error: Got unexpected extra arguments (two three)" in result.output


def test_persisting(tmpdir):
    """Test saving and reading url path_items from disk """

    test = UrlPattern(
        name="test",
        pattern="https://host{pattern1}/something{pattern2}.php",
        help_text="Test pattern",
    )
    test2 = UrlPattern(
        name="test2", pattern="https://athing.com", help_text="Another test pattern"
    )
    test3 = UrlPattern(
        name="test3",
        pattern="https://uniqcode_Привет.com",
        help_text="Another test pattern",
    )
    test4 = UrlPattern(name="test4", pattern="https://no_help")
    test5 = WildCardUrlPattern(name="test5", pattern="https://search{query}")

    patterns = URLPatternList(items=[test, test2, test3, test4, test5])

    test_file = tmpdir / "urlpatterns.yaml"
    with open(test_file, "w") as f:
        patterns.save(f)

    with open(test_file, "r") as f:
        text = f.read()

    with open(test_file, "r") as f:
        from_file = URLPatternList.load(f)

    assert len(patterns) == len(from_file)
    assert patterns[0].pattern == from_file[0].pattern
    assert patterns[2].pattern == from_file[2].pattern
    assert type(patterns[4]) == WildCardUrlPattern


def test_load_from_file():
    """Test load from file directly"""

    file = RESOURCE_PATH / "urlpatterns_example.yaml"

    with open(file, "r") as f:
        from_file = URLPatternList.load(f)

    assert from_file[2].pattern == "https://uniqcodeПривет.com"


def test_base_class():
    test = YeahYeahMenuItem(name="test")
    with pytest.raises(NotImplementedError):
        test.to_click_command()


def test_url_pattern_plugin(tmpdir):
    config_file = Path(tmpdir / "test_url_pattern_config.yaml")
    assert not config_file.exists()
    # file should be created if not exists
    plugin = UrlPatternsPlugin.__from_file_path__(config_file_path=config_file)
    assert config_file.exists()
    items = plugin.get_menu_items()

    assert len(items) == 3


def test_url_pattern_plugin_admin(yeahyeah_instance):
    runner = CliRunner()
    response = runner.invoke(
        yeahyeah_instance.root_cli, "admin url_patterns status".split(" ")
    )
    assert response.exit_code == 0
    assert "3 path_items in plugin" in response.output


def test_url_pattern_plugin_admin_add__remove_list_record(yeahyeah_instance):
    runner = CliRunner()
    url_pattern_plugin = yeahyeah_instance.plugins[0]

    assert len(url_pattern_plugin.pattern_list) == 3

    response = runner.invoke(
        yeahyeah_instance.admin_cli,
        "url_patterns add a_url https://host.{param1}/index.html".split(" ")
    )
    assert response.exit_code == 0
    assert len(url_pattern_plugin.pattern_list) == 4

    response = runner.invoke(yeahyeah_instance.admin_cli, "url_patterns list")

    assert response.exit_code == 0

    response = runner.invoke(
        yeahyeah_instance.admin_cli,
        "url_patterns remove a_url".split(" ")
    )
    assert response.exit_code == 0
    assert len(url_pattern_plugin.pattern_list) == 3


def test_url_pattern_plugin_admin_add_escape_all(yeahyeah_instance):
    """Make sure nothing in url gets interpreted except the {} patterns"""
    runner = CliRunner()
    url_pattern_plugin = yeahyeah_instance.plugins[0]

    assert len(url_pattern_plugin.pattern_list) == 3

    response = runner.invoke(
        yeahyeah_instance.admin_cli,
        "url_patterns add a_url https://host.{param1}/space%20index.html".split(" ")
    )
    assert response.exit_code == 0
    assert len(url_pattern_plugin.pattern_list) == 4

