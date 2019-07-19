from pathlib import Path
from logging import getLogger
from typing import (
    Optional,
    Union,
    Dict,
    Any,
    List,
    TextIO,
    Tuple,
    Iterable,
    cast,
    Callable,
)
from io import TextIOWrapper
from os import chdir, getcwd
import importlib.util
from datetime import datetime

import toml  # type: ignore
import jinja2

from .helper import ExistingFile, ExistingDir, InvalidVariant, HookModuleInterface
from .Plugin import Plugin, Flavour

build_hints_line_length = 88
# signature of any function specified inside a variant to be called after a successful
# build
HookFunction = Callable[["Schema", Iterable[Plugin]], None]

build_info_marker_begin = "  BEGIN OF BUILD INFORMATION  "
build_info_marker_end = "  END OF BUILD INFORMATION  "

build_info_template = """\
{comment_char}{comment_char} Constructed by `cobu - The configbuilder` at {date}

{comment_char}{comment_char} Do not change the following markers or information between them
{comment_char}{comment_char} as they are also used by `cobu change`
{marker_begin}
{build_info}
{marker_end}
"""


class Variant:
    def __init__(
        self,
        name: str,
        fragments: Iterable[str],
        fragments_basepath: ExistingDir,
        description: str = "",
        with_comments: bool = True,
    ) -> None:
        """
        :param fragments_basepath: Usually the path to fragments is relative to the
        schema file.
        """
        self.name = name
        self.fragments = fragments
        self.description = description.replace("\n", "").strip()
        self.with_comments = with_comments
        self.fragments_basepath = fragments_basepath

    def __repr__(self) -> str:
        return f"Variant(fragments={self.fragments}, description='{self.description}')"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.name, self.fragments) == (other.name, other.fragments)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name < other.name

    def build(self, plugins: Iterable[Plugin], comment_char: str = "#") -> str:
        """
        :return: The constructed config file        """
        jinja_environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.fragments_basepath))
        )
        build_info_parts = []
        for plugin in plugins:
            jinja_environment.globals.update({plugin.name: plugin.chosen_flavour})
            build_info_parts.append(
                f"{comment_char}{comment_char} {plugin.name}={plugin.chosen_flavour.name}"
            )
        build_info_str = "\n".join(build_info_parts)
        fragment_parts = [
            build_info_template.format(
                comment_char=comment_char,
                marker_begin=(
                    f"{comment_char}{comment_char}"
                    f"{build_info_marker_begin:{comment_char}^{build_hints_line_length-2}}"
                ),
                marker_end=f"{comment_char}{comment_char}{build_info_marker_end:{comment_char}^{build_hints_line_length-2}}",
                build_info=build_info_str,
                date=datetime.now().strftime("%c"),
            )
        ]
        for fragment in self.fragments:
            template = jinja_environment.get_template(str(fragment))
            if self.with_comments:
                fragment_parts.append(
                    # comment_char must occur at least twice at the beginning of the line
                    "{comment_char}{comment_char}{comment:{comment_char}^{line_length}}".format(
                        comment="  BEGIN: `{}`  ".format(fragment),
                        comment_char=comment_char,
                        # minus the one obligatory comment sign at the begin of the line
                        line_length=build_hints_line_length - 2,
                    )
                )
            fragment_parts.append(template.render())
            if self.with_comments:
                fragment_parts.append(
                    # comment_char must occur at least twice at the beginning of the line
                    "{comment_char}{comment_char}{comment:{comment_char}^{line_length}}".format(
                        comment="  END: `{}`  ".format(fragment),
                        comment_char=comment_char,
                        # minus the one obligatory comment sign at the begin of the line
                        line_length=build_hints_line_length - 2,
                    )
                )

        return "\n\n".join(fragment_parts)


class Schema:
    """
    Blabla
    """

    def __init__(
        self,
        path: ExistingFile,
        variants: Iterable[Variant],
        default_variant: Union[str, Variant],
        hook_module: Optional[HookModuleInterface],
        output_path: Union[str, Path] = "",
        comment_char: Union[str, bool] = "#",
    ) -> None:
        """
        Only used if all values are already known, for construction from a file have a
        look at `Schema.from_file`.
        :param comment_char: Used to enclose the path of the single fragments inside the
        build config file. If set to false no comments besides the from the fragments
        will be included. Useful if the target config does not allow any, if you still
        want to annotate your files use jinja2-comments
        :param output_path: Path to write the constructed file to.
        :param hook_module: Module containing hook functions to call after successful
        builds
        """
        self.path = path
        self.variants = {variant.name: variant for variant in variants}
        self.hook_module = hook_module
        _logger = getLogger(__name__)
        if isinstance(comment_char, bool):
            if not comment_char:
                for variant in self.variants.values():
                    variant.with_comments = False
            else:
                self.comment_char = "#"
        else:
            self.comment_char = comment_char
        if len(self.comment_char) < 1:
            raise ValueError("Comment character must include at least one character")
        if isinstance(default_variant, str):
            try:
                self.default_variant = self.variants[default_variant]
            except KeyError:
                raise ValueError(
                    "Default variant `name` does not match any names of "
                    f"variants of Schema {self.path}"
                )
        else:
            if not default_variant in self.variants.values():
                raise ValueError(
                    f"Passed default variant {default_variant} is no member of the "
                    "passed variants of "
                    f"Schema {self.path}"
                )
            self.default_variant = default_variant
        # check whether the schema defines its own output file, otherwise infer the name
        # of the target file from the stem of the schema file
        if not output_path:
            self.output_path = self.path.absolute().with_suffix("")  # type: Path
        else:
            self.output_path = self.path.parent / output_path
        self._chosen_variant: Optional[Variant] = None

    @property
    def chosen_variant(self) -> Variant:
        _logger = getLogger(__name__ + ".chosen_variant")
        if not self._chosen_variant:
            _logger.debug(
                "No variant for Schema `%s` chosen yet, using default one `%s`",
                self,
                self.default_variant,
            )
            return self.default_variant
        return self._chosen_variant

    @chosen_variant.setter
    def chosen_variant(self, value: Union[str, Variant]) -> None:
        if isinstance(value, str):
            try:
                self._chosen_variant = self.variants[value]
            except KeyError:
                raise InvalidVariant(
                    f"Chosen variant `{value}` does not match any names of "
                    f"variants specified of Schema {self}"
                )
        elif isinstance(value, Variant):
            if not value in self.variants.values():
                raise InvalidVariant(
                    f"Passed variant object {value} is no member of the variants of "
                    f"Schema {self}"
                )
            self._chosen_variant = value
        else:
            raise TypeError(
                "Chosen variant must either be a valid variant of the "
                f"Schema {self} or its name."
            )

    def __str__(self) -> str:
        return f"{self.path.parent / str(self.path)}"

    def __repr__(self) -> str:
        return str(self)

    def build(self, plugins: Iterable[Plugin]) -> str:
        """
        Build the chosen or default variant of this schema with the given plugins.
        :return: Constructed config file
        """
        _logger = getLogger(__name__ + ":build")
        _logger.debug("Building variant %s of schema %s", self.chosen_variant, self)
        return self.chosen_variant.build(plugins, self.comment_char)

    @classmethod
    def from_file(cls, filehandle: TextIO, no_hooks=False) -> "Schema":
        """
        Loads a schema from the given filehandle.
        :param filehandle: TextIO to read the schema content from.
        :param no_hooks: Whether to skip loading of any hook modules.
        :return: Loaded Schema
        """
        _logger = getLogger(__name__ + ":from_file")
        _logger.debug("Trying to load schema from %s", filehandle.name)
        try:
            schema_content = toml.loads(filehandle.read())
        except toml.TomlDecodeError as e:
            _logger.error("Could not load toml file, error has been: %s", e)
            exit(1)
        directory = ExistingDir(Path(filehandle.name).parent)

        try:
            variants = []
            for name, content in schema_content["variants"].items():
                _logger.debug("Processing Variant %s", name)
                try:
                    variants.append(
                        Variant(
                            name=name,
                            fragments=content["fragments"],
                            fragments_basepath=directory,
                            description=content.get("description", ""),
                        )
                    )
                except KeyError:
                    raise ValueError(
                        f"Variant {name} of Schema {filehandle.name} contains no "
                        "fragments."
                    )

        except KeyError:
            raise ValueError(f"Schema {filehandle.name} contains no variants.")
        hook_module = None
        if no_hooks:
            _logger.debug("Skipping loading of any hook modules as requested.")
        elif "hooks" in schema_content:
            _logger.debug("Trying to load hook module %s", schema_content["hooks"])
            hook_module = load_hook_module(directory / schema_content["hooks"])
        if hook_module:
            _logger.debug(
                "Successfully loaded hook module from %s", schema_content["hooks"]
            )

        try:
            schema = Schema(
                path=ExistingFile(filehandle.name),
                variants=variants,
                default_variant=schema_content["default_variant"],
                comment_char=schema_content["comment_char"],
                output_path=schema_content.get("output_path", ""),
                hook_module=hook_module,
            )
        except KeyError as e:
            raise ValueError(f"Schema {filehandle.name} is missing `{e}`")
        return schema


def load_hook_module(module_file: Path) -> Optional[HookModuleInterface]:
    _logger = getLogger(f"{__name__}.load_hook_module")
    spec = importlib.util.spec_from_file_location(
        str(module_file), location=str(module_file)
    )
    if spec is None:
        _logger.error("Specified hooks file `%s` could not be found", module_file)
        return None
    hook_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(hook_module)  # type: ignore
    except (SyntaxError, ModuleNotFoundError) as e:
        _logger.error("Could not compile `%s`. See debug log for traceback")
        _logger.debug("The error has been:", exc_info=True)
        return None
    except FileNotFoundError:
        _logger.error("Specified hooks file `%s` could not be found", module_file)
        return None
    return hook_module  # type: ignore
