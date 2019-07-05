"""
fritz.configuration
~~~~~~~~~~~~~~~~~~~

Helps manage fritz configuration.

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""

import os
from pathlib import Path
import configparser

import fritz
import fritz.errors


_HOME = str(Path.home())

if os.environ.get("FRITZ_CONFIG_PATH"):
    CONFIG_PATH = os.environ["FRITZ_CONFIG_PATH"]
else:
    CONFIG_PATH = os.path.join(_HOME, ".fritz")


def init_config(path=CONFIG_PATH):
    """Initializes Fritz configuration, by default checking ~/.fritz.

    If FRITZ_ENV environment variable is set, uses that section in config file.

    Args:
        path (str): Set path to override where config file is initialized from.
    """
    path = Path(path)

    if not path.exists():
        raise fritz.errors.MissingFritzConfigError(path)

    fritz_config = load_config_file(path=path)

    try:
        env = os.environ.get("FRITZ_ENV", "default")
        defaults = dict(fritz_config.items(env))
        fritz.configure(
            api_key=defaults["api_key"],
            project_id=defaults["project_id"],
            api_base=defaults.get("api_base"),
        )
    except (configparser.NoSectionError, KeyError):
        raise fritz.errors.InvalidFritzConfigError(path)


def load_config_file(path=CONFIG_PATH):
    """Loads configuration file from disk.

    Args:
        path (str): Path of config file to load.

    Returns: ConfigParser
    """
    fritz_config = configparser.ConfigParser()
    fritz_config.read(path)
    return fritz_config


def write_config_file(fritz_config, path=CONFIG_PATH):
    """Writes provide configuration file.

    Args:
        fritz_config (ConfigParser): Configuration to save.
        path (str): Path of destination config file.
    """
    fritz_config.write(open(path, "w"))


def get_credentials(fritz_config):
    """Gets credentials from config.

    Args:
        fritz_config (ConfigParser): Fritz Configuration.

    Returns: dict of credentials
    """
    env = os.environ.get("FRITZ_ENV", "default")
    return dict(fritz_config.items(env))


def update_credentials(fritz_config, **updates):
    """Updates Fritz config.

    Args:
        fritz_config (ConfigParser): Fritz Configuration.
        updates (dict): updates

    Returns: ConfigParser
    """
    env = os.environ.get("FRITZ_ENV", "default")
    try:
        defaults = get_credentials(fritz_config)
    except configparser.NoSectionError:
        defaults = {}

    defaults.update(updates)
    fritz_config[env] = defaults

    return fritz_config
