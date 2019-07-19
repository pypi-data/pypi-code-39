from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, Namespace
from typing import Optional, Iterable, TextIO, cast, Union, Dict
from pathlib import Path
from logging import getLogger
from json import loads, dumps
from inspect import isfunction
from sys import stdout

from .Base import Subcommand

from .. import __name__ as name
from ..Plugin import Plugin, Flavour
from ..helper import ExistingFile, InvalidVariant
from ..Schema import Schema, Variant
from ..config import config


class Builder(Subcommand):
    """Create a config file based on a schema file"""

    name = "build"
    help = __doc__
    description = __doc__

    def __init__(self) -> None:
        self.plugins = Plugin.from_directory(config.plugin_dir)

    def populate_subparser(self, subparser) -> None:
        """
        Receives a subparser to populate
        """
        subparser.add_argument(
            "schema",
            nargs="?",
            type=Path,
            default=Path.cwd(),
            help="""Path to schema file or a directory containing a schema file. If not
            given the local directory will be searched for one. The schema file must at
            least contain one variant and the special `build` section.""",
        )
        subparser.add_argument(
            "-v",
            "--variant",
            type=str,
            help="""One of the variants described in the schema file. If not given the default
            variant specified in the schema file will be used.""",
        )
        subparser.add_argument(
            "-o",
            "--output",
            type=FileType("w"),
            help="""Where to write the contructed file to. Overwrites the default
            mechanism of using the stem of the schema file and the possibility to
            specify the output file inside the schema.""",
        )
        subparser.add_argument(
            "--no-hooks",
            action="store_true",
            help="Do not execute any hooks specified in the schema",
        )
        subparser = self.populate_argparse(subparser)

        cache_args_group = subparser.add_argument_group(
            "Build information",
            f"""To support the `{name} change` functionality it
            is necessary to store the information of previous builds to determine which
            plugins or variants have changed. Per default those information are only
            stored if the config file has been written to the default output. The used
            file is {config.build_information_file}""",
        )

        cache_args = cache_args_group.add_mutually_exclusive_group()

        cache_args.add_argument(
            "--no-cache",
            action="store_true",
            help="Do not save build information despite output target",
        )
        cache_args.add_argument(
            "--cache",
            action="store_true",
            help="Save build information despite output target",
        )

        return subparser

    def populate_argparse(
        self,
        parser_to_populate: ArgumentParser,
        arg_group_title: str = "Plugins",
        arg_group_description: str = (
            "Every has Plugin has a default flavour which will be used if not specified "
            "otherwise"
        ),
    ) -> ArgumentParser:
        plugin_arg_group = parser_to_populate.add_argument_group(
            arg_group_title, arg_group_description
        )
        for plugin in self.plugins:
            plugin_arg_group.add_argument(
                f"--{plugin.name}",
                type=str,
                choices=plugin.flavours,
                help=plugin.description,
                default=plugin.default_flavour.name,
            )

        return parser_to_populate

    def main(self, args: Namespace) -> int:
        return self.build_schema(
            schema_path=args.schema,
            variant_to_build=args.variant,
            output=args.output,
            flavours={plugin.name: vars(args)[plugin.name] for plugin in self.plugins},
            cache=args.cache,
            no_cache=args.no_cache,
            no_hooks=args.no_hooks,
            quiet=args.quiet,
        )

    def build_schema(
        self,
        schema_path: Path,
        variant_to_build: Optional[Union[str, Variant]] = None,
        output: Optional[TextIO] = None,
        flavours: Optional[Dict[str, Union[str, Flavour]]] = None,
        cache=False,
        no_cache=False,
        quiet=False,
        no_hooks=False,
    ) -> int:
        _logger = getLogger(__name__ + ".main")
        # let's check whether we have been given a schema file
        if schema_path.is_file():
            schema = Schema.from_file(  # type: ignore # i know that this will open in text mode
                schema_path.open(), no_hooks
            )
        else:
            _logger.debug(
                "Passed schema path is not a file, using first match "
                "of `%s/*.schema`.",
                schema_path,
            )
            try:
                schema_file = (
                    list(schema_path.glob("*.schema"))[0].expanduser().absolute()
                )
                schema = Schema.from_file(  # type: ignore # i know that this will open in text mode
                    schema_file.open(), no_hooks
                )
            except IndexError:
                _logger.error("Could not detect any schema file")
                exit(1)
        self.schema = schema
        if variant_to_build:
            try:
                schema.chosen_variant = variant_to_build
            except InvalidVariant as e:
                _logger.error(
                    "%s. Valid variants are: %s", e, ", ".join(schema.variants)
                )
                return 1
        _logger.debug("Using variant %s", schema.chosen_variant)

        if flavours:
            for plugin in self.plugins:
                # TODO catch error in case of of invalid selections
                plugin.chosen_flavour = flavours[plugin.name]
        self._build_and_write_config(output, quiet)

        if cache or (not output and not no_cache):
            # only update cache if the default output has been used
            # or if requested explicitly
            # also skip if requested
            self._save_build_information(schema)
        else:
            _logger.debug(
                "Not saving build information as requested or because of "
                "non-default output."
            )

        if self.schema.hook_module and not no_hooks:
            # hook module is defined, let see wheter a `build` function is defined
            hook_module = self.schema.hook_module
            try:
                _logger.info(
                    "Calling `build` function of hook module %s", hook_module.__name__
                )
                hook_module.build(self.schema, {p.name: p for p in self.plugins})
            except AttributeError:
                # no build function defined, that's fine
                _logger.debug("Hook module has no `build` function")
            except TypeError:
                _logger.warning(
                    "Hook module contains a `build` attribute but it is not callable "
                    "or does not accept the two arguments: Schema and plugins."
                )
        return 0

    def _save_build_information(self, schema: Schema) -> None:
        _logger = getLogger(f"{__name__}.save_build_information")
        build_information_file = config.build_information_file

        try:
            build_information = loads(build_information_file.read_text())
        except FileNotFoundError:
            _logger.info(
                "Build information file `%s` does not exist yet.",
                build_information_file,
            )
            build_information = {}

        build_information.update(
            {
                str(schema): {
                    "variant": str(schema.chosen_variant),
                    "plugins": {p.name: str(p.chosen_flavour) for p in self.plugins},
                }
            }
        )

        build_information_file.write_text(dumps(build_information))
        _logger.info("Build information written to %s", build_information_file)

    def _build_and_write_config(self, output: Optional[TextIO], quiet=False) -> None:
        """
        Calls
        """
        built_config = self.schema.build(self.plugins)

        if output:
            output.write(f"{built_config}\n")
        else:
            self.schema.output_path.write_text(built_config + "\n")
        if not quiet:
            print(
                "Built config file has been written to",
                output.name if output else self.schema.output_path,
            )
    
