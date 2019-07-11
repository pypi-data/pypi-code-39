"""Contain utility functions."""

import getpass
import pathlib
import re
import typing as tp


DATE_PATTERN = re.compile(r"(\d{,2})/(\d{,2})/(\d{4}) (\d{,2}):(\d{2}):(\d{2})")


def compile_regex() -> tp.List[re.compile]:
    """Return compiled regex patterns.

    These patterns are used to try to match episode numbers in order to tag
    episodes.
    """
    return [
        re.compile(r"EPISODE #?(\d+)", re.IGNORECASE),
        re.compile(r"#?(\d+)", re.IGNORECASE),
        re.compile(r"^Show (\d+)", re.IGNORECASE),
        re.compile(r"Ep\.? (\d+)", re.IGNORECASE),
    ]


def get_episode_number(title: str) -> str or None:
    """Attempt to parse episode number out of a title.

    This is functionally identical
    """
    for pattern in compile_regex():
        match = pattern.search(title)
        if match:
            return match.groups()[0]


def get_directory(name: str, default: pathlib.Path) -> pathlib.Path:
    """Prompt user for directory, create and then return path."""
    while True:
        prompt = f"{name} (Leave blank for {default}): "
        raw_input = input(prompt)
        if not raw_input:
            path = default
        elif raw_input[0] == "~":
            path = pathlib.Path("~").expanduser()
            try:
                if raw_input[1] == "/":
                    path /= raw_input[2:]
            except IndexError:
                pass  # Catch case where user enters just `~` or `~/`
        else:
            path = pathlib.Path(raw_input)
        try:
            path.mkdir(exist_ok=True, parents=True)
            return path
        except (IOError, PermissionError, OSError) as err:
            print(f"Invalid directory: {err}")


def get_credentials(prompt: str) -> tp.Tuple[str, str]:
    """Display prompt, return username and password"""
    print(prompt)
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    return username, password


def date_handler(a_date_string):
    """Parse a UTC date in MM/DD/YYYY HH:MM:SS format."""
    search = DATE_PATTERN.search(a_date_string)
    if search:
        month, day, year, hour, minute, second = search.groups()
        return (
            int(year),
            int(month),
            int(day),
            int(hour),
            int(minute),
            int(second),
            0,
            0,
            0,
        )
