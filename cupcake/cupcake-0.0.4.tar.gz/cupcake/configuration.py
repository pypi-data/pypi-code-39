"""A configuration holds all the parameters to build a package.

Variables fall into a few different categories:

- ABI variables, e.g. architecture, operating system, compiler, C++ standard.
  These variables must be shared among all packages linked together.
- Package variables, i.e. options. These variables control aspects of building
  a specific package (which might be a dependency).
- Tool variables, e.g. build and install directories, or generator. These
  variables control how the tools work, but do not affect the ABI.
"""

import os
from pathlib import Path
import typing as t

from cached_property import cached_property  # type: ignore


class DictObject:
    """An object that takes its attributes from a :class:`dict`."""

    def __init__(self, variables):
        self.variables = variables

    def __getattr_(self, name):
        value = self.variables[name]
        return DictObject(value) if isinstance(value, t.Mapping) else value


class CMakeConfiguration(DictObject):

    @cached_property
    def directory(self) -> Path:
        """The build directory as an absolute path."""
        return Path(self.variables.get('directory', '.build')).resolve()

    @cached_property
    def prefix(self) -> Path:
        """The installation prefix as an absolute path."""
        return Path(self.variables.get('prefix', '.install')).resolve()

    @cached_property
    def generator(self):
        return 'Ninja'


class Configuration(DictObject):

    @cached_property
    def cmake(self):
        return CMakeConfiguration(self.variables.get('cmake', {}))
