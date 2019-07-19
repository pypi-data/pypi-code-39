"""Dedicated to any interaction with Plugins."""

from pathlib import Path
from typing import (
    List,
    Dict,
    Optional,
    TextIO,
    Union,
    Callable,
    cast,
    Any,
    Iterable,
    Mapping,
    Set,
)
from logging import getLogger
from os import PathLike
from collections import UserDict
from argparse import ArgumentParser
from functools import lru_cache

from .helper import ExistingDir, InvalidFlavour


class Flavour(UserDict):
    """
    A plugin can occur in different flavours, enabling a color plugin to provide
    multiple colorschemes which can be exchanged.
    """

    def __init__(self, name: str, initialdata: Dict[str, Any] = None) -> None:
        _logger = getLogger(__name__ + ":Flavour")
        super().__init__(initialdata)
        self.name = name
        _logger.debug("Constructed Flavour %s", self.name)

    def __hash__(self) -> int:
        return hash(tuple((key, value) for key, value in sorted(self.items())))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.name == other.name

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name < other.name

    def __str__(self) -> str:
        return self.name

    def create_alias(self, alias: str) -> "Flavour":
        """
        Create an alias of this flavour with a different name
        """
        _logger = getLogger(__name__ + ":create_alias")
        _logger.debug("Creating alias of %s: %s", self.name, alias)
        return Flavour(alias, initialdata=self.data)


class Plugin:
    def __init__(
        self,
        name: str,
        flavours: Iterable[Flavour],
        default_flavour: Union[str, Flavour],
        aliases: Optional[Mapping[str, str]] = None,
        description: str = "",
    ) -> None:
        self.name = name
        self.description = description
        self.flavours = {flavour.name: flavour for flavour in flavours}
        self.aliases = aliases
        if isinstance(default_flavour, str):
            try:
                self.default_flavour = self.flavours[default_flavour]
            except KeyError:
                raise ValueError(
                    f"Default flavour `{name}` does not match any name of "
                    f"flavours of Plugin {self}"
                )
        else:
            if default_flavour not in self.flavours.values():
                raise ValueError(
                    f"Passed default flavour {default_flavour} is no member of the "
                    "passed flavours of "
                    f"Plugin {self}"
                )
            self.default_flavour = default_flavour
        _logger = getLogger(__name__)
        if self.aliases:
            for alias, existing in self.aliases.items():
                try:
                    self.flavours.update(
                        {alias: self.flavours[existing].create_alias(alias)}
                    )
                except KeyError:
                    _logger.warning(
                        "Not creating flavour alias %s in Plugin %s "
                        "since the target `%s` does not exist",
                        alias,
                        self,
                        existing,
                    )
        self._chosen_flavour: Optional[Flavour] = None

    @property
    def chosen_flavour(self) -> Flavour:
        _logger = getLogger(__name__ + ".chosen_flavour")
        if not self._chosen_flavour:
            _logger.debug(
                "Plugin `%s` has no chosen flavour, using default one `%s`",
                self,
                self.default_flavour,
            )
            return self.default_flavour
        return self._chosen_flavour

    @chosen_flavour.setter
    def chosen_flavour(self, value: Union[str, Flavour]) -> None:
        if isinstance(value, str):
            try:
                self._chosen_flavour = self.flavours[value]
            except KeyError:
                raise InvalidFlavour(
                    f"Chosen flavour {value} does not match any names of "
                    f"flavours of Plugin {self}"
                )
        elif isinstance(value, Flavour):
            if value not in self.flavours.values():
                raise InvalidFlavour(
                    f"Passed chosen flavour {value} is no member of the flavours of "
                    f"Plugin {self}"
                )
            self._chosen_flavour = value
        else:
            raise TypeError(
                "Chosen flavour must either be a valid flavour of the "
                "Plugin {self} or its name."
            )

    def __str__(self) -> str:
        return f"Plugin({self.name}) with flavours: [{','.join(self.flavours)}]"

    def __repr__(self) -> str:
        return f"Plugin({self.name})"

    @staticmethod
    def _from_json_file(filehandle: TextIO) -> "Plugin":
        pass

    @staticmethod
    def _from_toml_file(filehandle: TextIO) -> "Plugin":
        _logger = getLogger(__name__)
        try:
            from toml import loads  # type: ignore
        except ImportError:
            _logger.exception("`python-toml` is needed for loading toml files.")

        toml_file = loads(filehandle.read())
        try:
            flavours = [
                Flavour(name, data) for name, data in toml_file["flavours"].items()
            ]
            plugin = Plugin(
                name=Path(filehandle.name).stem,
                flavours=flavours,
                default_flavour=toml_file["default"],
                aliases=toml_file.get("aliases", []),
                description=toml_file["description"],
            )
        except KeyError as e:
            raise ValueError(f"Schema {filehandle.name} is missing table {e}.")

        return plugin

    @classmethod
    def from_file(cls, filehandle: TextIO, extension: str = "") -> "Plugin":
        """
        :param filehandle: An open filehandle to load the  Plugin from.
        :param extension: Extension of the file if it cannot be infered from the
        filehandle (with leading dot).
        """
        file_loaders: Dict[str, Callable[[TextIO], "Plugin"]] = {
            ".toml": cls._from_toml_file,
            ".json": cls._from_json_file,
        }
        try:
            ext = extension or Path(filehandle.name).suffix
            loader = file_loaders[ext]
            return loader(filehandle)

        except KeyError:
            raise NotImplementedError(
                f"Inferred extension {ext} is not supported, try to pass the "
                "extension as additional parameter."
            )

    @staticmethod
    @lru_cache()
    def from_directory(plugin_dir: Path, recursive: bool = False) -> Set["Plugin"]:
        """
        Given a directory load try to load all files which are supported by any loader
        of the Plugin class.
        :param directory: Directory to look for plugin files.
        :param recursive: Whether to recurse into the directory.
        """
        # using a set to eliminate any possibility of duplicates
        _logger = getLogger(__name__ + ":from_directory")
        directory = ExistingDir(plugin_dir)
        plugins: Set["Plugin"] = set()
        _logger.debug("Looking for plugins in directory %s", directory)
        for path in directory.iterdir():
            if recursive and path.is_dir():
                _logger.debug("Recursing into child directory %s", path)
                plugins |= Plugin.from_directory(path, True)
            elif path.is_file():
                try:
                    _logger.debug("Will try to load plugin from %s", path)
                    with open(path) as file:
                        plugins.add(Plugin.from_file(file))
                except NotImplementedError:
                    _logger.debug(
                        "Could not load plugin from %s since its extension %s "
                        "is not supported (yet)",
                        path,
                        path.suffix,
                    )
                except ValueError as e:
                    _logger.error(
                        "Could not load plugin from file %s since the "
                        "following error occurred: %s",
                        path,
                        e,
                    )

        return plugins
