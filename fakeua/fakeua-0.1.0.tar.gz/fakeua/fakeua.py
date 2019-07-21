#!/usr/bin/env python3

from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError

from pathlib import Path

from json import dump, load

from typing import Any, Dict, List, Optional

from random import choice


DEFAULT_JSON_FP: Path = Path().home() / ".fakeua_databrowsers.json"
DEFAULT_VERSION_FILTER = "rv:6"
DEFAULT_BROWSER = "firefox"


def fake_useragent_load_ua() -> Optional[UserAgent]:
    """Try to load UA fake-useragent object, catching it's exception."""
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        ua = None
    return ua


def update_useragent_db(path: Path = DEFAULT_JSON_FP) -> bool:
    """Save ua.data_browsers dict in a json file."""
    ua = fake_useragent_load_ua()
    if ua:
        with open(path, "w") as json_file:
            dump(ua.data_browsers, json_file)
        return True
    else:
        return False


def load_useragent_db(
    path: Path = DEFAULT_JSON_FP
        ) -> Optional[Dict[Any, Any]]:
    """Load json data_browsers file."""
    if path.exists():
        with open(path, "r") as json_file:
            data = load(json_file)
        return data
    else:
        return None


def get_useragent_list(
    browser: str = DEFAULT_BROWSER,
    version_filter: str = DEFAULT_VERSION_FILTER,
    path: Path = DEFAULT_JSON_FP
        ) -> List[Any]:
    """Get useragent list with the desired parameters."""
    data_browsers = load_useragent_db()
    if data_browsers:
        if browser in data_browsers.keys():
            return [i for i in data_browsers[browser] if version_filter in i]
        else:
            raise Exception("Invalid browser specified.")
    else:
        raise Exception("UserAgent object not present.")


def get_random_ua(
    browser: str = DEFAULT_BROWSER,
    version_filter: str = DEFAULT_VERSION_FILTER,
    path: Path = DEFAULT_JSON_FP
        ) -> str:
    """Get useragent list with the desired parameters."""
    return choice(
        get_useragent_list(
            browser=browser,
            version_filter=version_filter,
            path=path
            )
        )
