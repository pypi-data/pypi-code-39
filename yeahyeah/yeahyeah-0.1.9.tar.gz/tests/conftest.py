"""pytest fixtures shared by modules in this folder

"""
import webbrowser
from unittest.mock import Mock

import pytest

from plugins.path_items import PathItem, PathItemList, PathItemPlugin
from yeahyeah.core import YeahYeah
from plugins.url_patterns import URLPatternList, UrlPattern, WildCardUrlPattern, UrlPatternsPlugin


@pytest.fixture()
def url_pattern_list():
    """A pattern list with some content"""
    return URLPatternList(
        items=[
            UrlPattern(
                name="test1", pattern="https://host{pattern1}/something{pattern2}.php"
            ),
            UrlPattern(
                name="test2",
                pattern="https://athing.com",
                help_text="Another test pattern",
            ),
            WildCardUrlPattern(name="test5", pattern="https://search{query}"),
        ]
    )


@pytest.fixture()
def path_item_list():
    return PathItemList(items=[
        PathItem(
            name="home",
            path="/home/a_user/",
            help_text="(Example) Open home directory",
        ),
        PathItem(
            name="external_disk",
            path="/mnt/some_mount/user/something",
            help_text="(Example) Open that external disk",
        )
    ])

@pytest.fixture()
def yeahyeah_instance(url_pattern_list, path_item_list):
    """An instance of the yeahyeah launch manager with some default plugins and commands"""
    yeahyeah = YeahYeah()
    yeahyeah.add_plugin(UrlPatternsPlugin(pattern_list=url_pattern_list))
    yeahyeah.add_plugin(PathItemPlugin(item_list=path_item_list))

    return yeahyeah


@pytest.fixture()
def mock_web_browser(monkeypatch):
    """Mock the python standard webbrowser
    """
    mock_web_browser = Mock(spec=webbrowser)
    monkeypatch.setattr("plugins.url_patterns.webbrowser", mock_web_browser)
    return mock_web_browser
