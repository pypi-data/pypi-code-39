import argparse
from .exceptions import CommandError, ConfigurationError
from .commands import commands
from logging import getLogger

logger = getLogger(__name__)


def setup_arg_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    for command in commands:
        command_parser = subparsers.add_parser(command.name, description=command.__doc__)
        command.initialize_parser(command_parser)
        command_parser.set_defaults(main=command.main)
    return parser


def main():
    parser = setup_arg_parser()
    args = parser.parse_args()
    try:
        if not hasattr(args, 'main'):
            raise CommandError(f'Wrong command. Supported commands: {[command.name for command in commands]}')
        args.main(args)
    except (CommandError, ConfigurationError) as e:
        logger.exception(f'Start up failed')
