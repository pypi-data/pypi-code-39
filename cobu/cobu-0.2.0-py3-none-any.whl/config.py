from collections import ChainMap
from functools import lru_cache
from glob import glob
from logging import getLogger
from os import environ
from os.path import expanduser, expandvars
from pathlib import Path
from typing import Any, Hashable, Iterable, Optional, Set

import toml  # type: ignore

from . import __name__ as name
from .helper import ExistingDir


class _Config:
    default_config = {
        "plugin_dir": f"$XDG_CONFIG_HOME/{name}/plugins",
        "schema_globs": ["$XDG_CONFIG_HOME/**/*.schema"],
        "cache_dir": f"$XDG_CACHE_HOME/{name}",
    }

    def __init__(self, config_path=f"$XDG_CONFIG_HOME/{name}/config"):
        _Config.inject_xdg_fallbacks()
        _logger = getLogger(__name__)
        config_path = expanduser(expandvars(config_path))
        try:
            with open(config_path) as config_file:
                self.user_config = toml.load(config_file)
        except FileNotFoundError as e:
            _logger.info(
                "Could not load user config from `%s`, using default config. "
                "See `cobu dump default-config`.",
                config_path,
            )
            self.user_config = {}

        self.plugin_dir = Path(self.user_or_default("plugin_dir"))
        self.cache_dir = Path(self.user_or_default("cache_dir"))
        # make sure our cache directory always exists
        self.cache_dir.mkdir(mode=0o755, exist_ok=True)
        self.build_information_file = self.cache_dir / "build_information"

    def user_or_default(self, name: str) -> Any:
        """
        Return the config value if set by user and otherwise its default value.
        All environment variables and user tilde homes are resolved.
        """
        _logger = getLogger(__name__)

        def _expanded(s):
            if isinstance(s, str):
                return expandvars(expanduser(s))
            elif isinstance(s, Iterable):
                return [expanduser(expandvars(_s)) for _s in s]

        if name in self.user_config:
            _logger.debug(
                "Found `%s` in user config, using `%s`", name, self.user_config[name]
            )
            return _expanded(self.user_config[name])
        _logger.debug(
            "`%s` not specified in user config, using default value `%s`",
            name,
            _Config.default_config[name],
        )
        return _expanded(_Config.default_config[name])

    @property
    def schema_globs(self) -> Set[str]:
        return _Config._resolve_glob_paths(tuple(self.user_or_default("schema_globs")))

    @staticmethod
    def inject_xdg_fallbacks() -> None:
        """
        Injects the fallback values of XDG variables into the environment to ease
        handling of them
        """
        xdg_env_var_defaults = {
            "XDG_CONFIG_HOME": "~/.config",
            "XDG_CACHE_HOME": "~/.cache",
        }
        for var, fallback in xdg_env_var_defaults.items():
            if not var in environ:
                environ[var] = expanduser(fallback)

    @staticmethod
    @lru_cache()
    def _resolve_glob_paths(globs: Iterable[str]) -> Set[str]:
        """
        Resolves all given globs and caches the result which is why the passed Iterable has
        to be hashable. Recursive globs are recognized and resolved.
        :param globs: A single glob or an hashable iterable of multiple.
        :return: Set of resolved globs
        """

        def resolve_single_glob(_glob: str) -> Set[str]:
            return set(glob(expandvars(expanduser(_glob)), recursive="**" in _glob))

        if isinstance(globs, str):
            return resolve_single_glob(globs)

        resolved_globs: Set[str] = set()
        for g in globs:
            resolved_globs |= resolve_single_glob(g)

        return resolved_globs


config = _Config()
