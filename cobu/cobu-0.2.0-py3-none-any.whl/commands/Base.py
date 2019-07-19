from __future__ import annotations

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from logging import getLogger
from typing import ClassVar, Dict, List, Type

registered_subcommands: Dict[str, Type[Subcommand]] = {}


class Subcommand:
    """Base class for all subcommands.

    All subcommands are initiated before their methods are called but their custom
    constructor cannot receive any arguments.
    """

    name: ClassVar[str] = ""
    """Name of the command in the command line interface.
    """
    help: ClassVar[str] = ""
    """Help message to add to the command line interface.
    """

    description = ""

    aliases: ClassVar[List[str]] = []
    """List of aliases to use for this subcommand in the command line interface.
    """

    formatter_class = ArgumentDefaultsHelpFormatter
    """Custom formatter class of this subcommand if a custom one is required.
    """

    def __init_subclass__(cls):
        _logger = getLogger(__name__)
        if cls.name in registered_subcommands:
            _logger.warning(
                "Subcommand %s already registered by class %s. Skipping class %s",
                cls.name,
                registered_subcommands[cls.name],
                cls,
            )
            return
        registered_subcommands[cls.name] = cls

    def populate_subparser(self, subparser: ArgumentParser) -> None:
        """
        Receives a subparser object to populate with the needed arguments of this
        subcommand.

        :param subparser:
        """
        raise NotImplementedError

    def main(self, args: Namespace) -> int:
        """
        Execute the subcommand.
        :param args: All parsed command line arguments
        """
        raise NotImplementedError
