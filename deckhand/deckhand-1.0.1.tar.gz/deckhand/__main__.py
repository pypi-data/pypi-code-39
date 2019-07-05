#!/usr/bin/env python3
# Copyright 2019 The Deckhand Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run deckhand from the command line."""

import sys
import logging
import argparse

from termcolor import colored
from deckhand.__about__ import __version__, __name__
from deckhand.util.logger import start_logging
from deckhand.commands.list import list_tools
from deckhand.commands.update import update_tools
# from deckhand.commands.initialize import initialize_project
from deckhand.commands.install import install_all
from deckhand.commands.configure import configure_stable, configure_dev, configure_clear, configure_list

def main(arguments=None):
    """
    Get arguments, initialize logger, and execute any commands.

    :param args: Arguments to use if not using console arguments.
    """
    if arguments is None:
        arguments = sys.argv[1:]

    parser = argparse.ArgumentParser(
            prog=__name__
    )

    parser.add_argument('-v', '--verbose',
            action='store_true',
            help='give more console output')

    parser.add_argument('-V', '--version',
            action='store_true',
            help='show version and exit')

    subparsers = parser.add_subparsers(title='commands', metavar="<command>")

    config_parser = subparsers.add_parser('config', help='manage pip configurations')
    config_subparsers = config_parser.add_subparsers(title='configurations', metavar="<configuration>")
    config_dev_parser = config_subparsers.add_parser('dev', help='set pip configuration for development')
    config_dev_parser.set_defaults(execute=configure_dev)
    config_stable_parser = config_subparsers.add_parser('stable', help='set pip configuration for stable releases')
    config_stable_parser.set_defaults(execute=configure_stable)
    config_list_parser = config_subparsers.add_parser('list', help='show current pip configuration')
    config_list_parser.set_defaults(execute=configure_list)
    config_reset_parser = config_subparsers.add_parser('reset', help='reset pip configuration to defaults')
    config_reset_parser.set_defaults(execute=configure_clear)

    # env_parser = subparsers.add_parser('env', help='manage a Python virtualenv')
    # env_subparsers = env_parser.add_subparsers(title='commands')
    # env_init_parser = env_subparsers.add_parser('init', help='initialize virtual environment in working directory')
    # env_init_parser.set_defaults()
    # env_activate_parser = env_subparsers.add_parser('activate', help='activate virtual environment in working directory')
    # env_activate_parser.set_defaults()

    # init_parser = subparsers.add_parser('init', help='initialize a fresh project')
    # init_parser.add_argument('project_type'
    
    # )
    # init_parser.set_defaults(execute=initialize_project)

    install_parser = subparsers.add_parser('install', help='install external tools', add_help=False)
    install_parser.set_defaults(execute=install_all)

    # # license_parser = subparsers.add_parser('license', help='add LICENSE file and headers to project')

    list_parser = subparsers.add_parser('list', help='list external tools', add_help=False)
    list_parser.set_defaults(execute=list_tools)

    update_parser = subparsers.add_parser('update', help='update external tools', add_help=False)
    update_parser.set_defaults(execute=update_tools)

    commands = parser.parse_args(arguments)

    if commands.version:
        print(__name__ + ' ' + __version__)
        exit(0)

    start_logging(commands.verbose)
    logging.debug(colored(commands, 'green'))

    try:
        commands.execute(commands)
    except AttributeError as error:
        logging.debug(colored(error, 'green'))

    exit(0)


if __name__ == '__main__':
    main()
