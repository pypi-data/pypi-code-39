import logging
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from typing import Dict


def main() -> int:
    from .config import config

    from .commands.Base import Subcommand, registered_subcommands

    parser = ArgumentParser(
        description=(
            "Cobu enables you to build your config files from multiple fragments "
            "as well as using plugins (e.g. different colorschemes)."
        ),
        formatter_class=ArgumentDefaultsHelpFormatter,
        epilog="GPLv3+",
    )
    verbosity_args = parser.add_mutually_exclusive_group()
    verbosity_args.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help=(
            "Show debug messages once command line arguments have been parsed. "
            "To show debug messages during initialisation set the environment variable "
            "CONFIGBUILDER_DEBUG."
        ),
    )
    verbosity_args.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Do not show any messages except errors.",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        title="Subcommands",
        help="The functionality is split over multiple subcommands",
    )

    commands: Dict[str, Subcommand] = {}

    for name, subcommand in registered_subcommands.items():
        subparser = subparsers.add_parser(
            subcommand.name,
            help=subcommand.help,
            description=subcommand.description,
            aliases=subcommand.aliases,
            formatter_class=subcommand.formatter_class,
        )
        cmd = subcommand()
        commands[name] = cmd
        cmd.populate_subparser(subparser)

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.quiet:
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)
    _logger = logging.getLogger(__name__)
    _logger.debug("Received args: {}".format(args))

    if args.command in commands:
        exit(commands[args.command].main(args))
    else:
        parser.print_usage()
        return 1


if __name__ == "__main__":
    exit(main)
