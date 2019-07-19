from pathlib import Path, _windows_flavour, _posix_flavour  # type: ignore
import os
from typing import Dict
from os.path import expanduser


class ExistingFile(Path):
    _flavour = _windows_flavour if os.name == "nt" else _posix_flavour

    def __init__(self, *args, **kwargs):
        super().__init__()
        if not self.is_file():
            raise ValueError(f"{self} is a directory.")
        if not self.exists():
            raise ValueError(f"{self} does not exist.")


class ExistingDir(Path):
    _flavour = _windows_flavour if os.name == "nt" else _posix_flavour

    def __init__(self, *args, **kwargs):
        super().__init__()
        if not self.is_dir():
            raise ValueError(f"{self} is not a directory.")
        if not self.exists():
            raise ValueError(f"{self} does not exist.")


class InvalidVariant(ValueError):
    pass


class InvalidFlavour(ValueError):
    pass


class HookModuleInterface:
    __name__: str

    @staticmethod
    def build(schema: "Schema", plugins: Dict[str, "Plugin"]):  # type: ignore
        ...
