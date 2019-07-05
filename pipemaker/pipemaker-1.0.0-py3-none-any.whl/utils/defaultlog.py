"""
enables one liner to create a logger with default settings

usage:
    from pipemaker.utils.defaultlog import log
"""
from logging.config import dictConfig
import yaml
from os.path import expanduser, join
dictConfig(yaml.load(open(join(expanduser("~"), "logging.yaml"))))
import logging
log = logging.getLogger()