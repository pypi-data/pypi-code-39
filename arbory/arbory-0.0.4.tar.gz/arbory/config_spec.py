"""Defines functionality for getting configuration specifications.
"""

import configparser
import pathlib


def config_spec():
    config = configparser.ConfigParser()
    config.read(pathlib.Path(__file__).parent / 'config.ini')
    selected = config['DEFAULT']['selected']
    return config[selected]
