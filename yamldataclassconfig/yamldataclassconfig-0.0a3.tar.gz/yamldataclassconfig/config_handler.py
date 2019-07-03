import os
import shutil
from pathlib import Path
from typing import Union


class YamlDataClassConfigHandler:
    """This class handles config.yml."""
    PATH_REFERENCE_DIRECTORY = Path(os.getcwd())
    PATH_TEST_DIRECTORY: Path = Path('tests')
    FILE_TARGET: Path = Path('config.yml')
    FILE_SOURCE: Path = Path('config.yml.dist')
    FILE_BACKUP: Path = Path('config.yml.bak')

    @classmethod
    def set_up(cls, file_source: Union[Path, str] = None):
        if file_source is None:
            file_source = cls.file_source()
        """This function set up config.yml."""
        if cls.file_target().is_file():
            shutil.move(str(cls.file_target()), str(cls.file_backup()))
        shutil.copy(str(file_source), str(cls.file_target()))

    @classmethod
    def do_cleanups(cls):
        """This function clean up config.yml."""
        if cls.file_backup().is_file():
            os.unlink(str(cls.file_target()))
            shutil.move(str(cls.file_backup()), str(cls.file_target()))

    @classmethod
    def file_target(cls) -> Path:
        return cls.path_target() / cls.FILE_TARGET

    @classmethod
    def file_source(cls) -> Path:
        return cls.path_source() / cls.FILE_SOURCE

    @classmethod
    def file_backup(cls) -> Path:
        return cls.path_target() / cls.FILE_BACKUP

    @classmethod
    def path_target(cls) -> Path:
        return cls.PATH_REFERENCE_DIRECTORY

    @classmethod
    def path_source(cls) -> Path:
        return cls.PATH_REFERENCE_DIRECTORY / cls.PATH_TEST_DIRECTORY
