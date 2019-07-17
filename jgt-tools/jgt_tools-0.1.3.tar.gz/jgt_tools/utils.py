"""Shared util functions."""
from collections import defaultdict
import csv
from pathlib import Path
import shlex
import subprocess

import tomlkit


DEFAULTS_FILE = Path(__file__).parent / "data" / "defaults.csv"


def execute_command_list(commands_to_run, verbose=True):
    """
    Execute each command in the list.

    If any command fails, print a helpful message and exit with that status.
    """
    for command in commands_to_run:
        if verbose:
            print(f"+{command}")
        subprocess.run(shlex.split(command), check=True)


_DEFAULT_CONFIGS: defaultdict = defaultdict(list)


def _load_defaults():
    with DEFAULTS_FILE.open() as f:
        for group, cmd in csv.reader(f):
            _DEFAULT_CONFIGS[group].append(cmd)


_load_defaults()


def load_configs():
    """Build configs from defaults and pyproject.toml."""
    package_root_path = Path(
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], universal_newlines=True
        ).split("\n")[0]
    )
    pyproject_path = package_root_path / "pyproject.toml"
    if not pyproject_path.exists():
        raise FileNotFoundError(
            f"Config file not found at: '{pyproject_path}' "
            "(must be run from project root)"
        )
    with pyproject_path.open() as f:
        pyproject = tomlkit.loads(f.read())

    poetry = pyproject["tool"]["poetry"]
    package_name = poetry["name"]
    package_description = poetry["description"]

    configs = {
        **_DEFAULT_CONFIGS,
        "package_name": package_name,
        "description": package_description,
        "base_dir": package_root_path,
    }
    if "jgt_tools" in pyproject["tool"]:
        configs = {**configs, **pyproject["tool"]["jgt_tools"]}
    return configs


CONFIGS = load_configs()
