# -*- coding: utf-8 -*-

"""Console script for amtool."""
import os
import sys
import importlib
import click
import logging
import click_log
from pkg_resources import iter_entry_points
from click_plugins import with_plugins


click_log.basic_config()


# Define Entry Point Command
@with_plugins(iter_entry_points('amt.plugins'))
@click.group()
@click_log.simple_verbosity_option(default='WARNING')
def main(args=None):
    """Console script for amtool."""
    logging.info('A message')
    return 0


# Load Commands from Subdirectories
SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
for m in next(os.walk(SCRIPT_PATH))[1]:
    try:
        commands = importlib.import_module(f"amt.{m}.command")
        for command in [c for c in importlib.import_module(
                f"amt.{m}.command").__dict__.values() if isinstance(
                    c, click.core.Command)]:
            main.add_command(command)
    except ModuleNotFoundError:
        pass


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
