from argparse import ArgumentDefaultsHelpFormatter, Namespace
from textwrap import indent
from typing import Iterable

from cobu.config import config
from cobu.Plugin import Plugin
from cobu.Schema import Schema

from .Base import Subcommand

_plugin_list_template = "{name}: {description} ({flavours})"


class Lister(Subcommand):
    """
    List all available Schemas and/or Plugins.
    """

    name = "list"
    help = __doc__
    description = __doc__
    # aliases=["li"],
    formatter_class = ArgumentDefaultsHelpFormatter

    def __init__(self) -> None:
        self.plugins = Plugin.from_directory(config.plugin_dir)

    def populate_subparser(self, subparser) -> None:
        subparser.add_argument(
            "object",
            help="Which kind of object should be listed.",
            choices=["plugins", "schemas"],
        )

    def main(self, args: Namespace) -> int:
        if args.object == "plugins":
            for plugin in self.plugins:
                flavours = []
                for flavour in sorted(plugin.flavours.values()):
                    if flavour == plugin.chosen_flavour:
                        flavour_str = f"[{flavour}]"
                    else:
                        flavour_str = str(flavour)
                    flavours.append(flavour_str)
                print(
                    _plugin_list_template.format(
                        name=plugin.name,
                        description=plugin.description.replace("\n", " "),
                        flavours=", ".join(flavours),
                    ),
                    "\t",
                )

        if args.object == "schemas":
            for schema_path in config.schema_globs:
                with open(schema_path) as file:
                    schema = Schema.from_file(file)
                print(schema_path)

        return 0
