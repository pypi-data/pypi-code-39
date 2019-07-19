from argparse import ArgumentParser, Namespace
from logging import getLogger

from ..config import config
from .Base import Subcommand


class Dumper(Subcommand):
    """Dump different internal files or states"""

    name = "dump"
    help = __doc__
    description = __doc__

    def populate_subparser(self, subparser: ArgumentParser) -> None:
        subparser.add_argument(
            "object",
            choices=["default_config", "build_information", "schema_paths"],
            help="""The `default_config` is in TOML format and can be used as is. The
            `build_information` are in JSON format. `schema_paths` is a newline
            separated list of detected schema paths.""",
        )

    def main(self, args: Namespace) -> int:
        _logger = getLogger(f"{__name__}.main")
        if args.object == "default_config":
            from toml import dumps  # type: ignore

            print(dumps(config.default_config))
        elif args.object == "build_information":

            build_information_file = config.build_information_file
            if not build_information_file.exists():
                _logger.warning("No build information saved yet")
                print("{}")
                return 1
            print(build_information_file.read_text())
        elif args.object == "schema_paths":
            print("\n".join(config.schema_globs))
        return 0
