"""This module implements fixture file handler."""
import os
import shutil
from typing import NoReturn

from fixturefilehandler.exceptions import BackupAlreadyExistError
from fixturefilehandler.file_paths import DeployFilePathInterface, VacateFilePathInterface


class FixtureFileHandler:
    """This class implements base functions."""
    @staticmethod
    def vacate_target_if_exist(file_path: VacateFilePathInterface) -> NoReturn:
        """
        This method vacate target file if target file exist.
        :return: No return
        """
        if file_path.backup.exists():
            raise BackupAlreadyExistError()
        if file_path.target.is_file():
            os.replace(str(file_path.target), str(file_path.backup))

    @staticmethod
    def deploy_resource(file_path: DeployFilePathInterface) -> NoReturn:
        """
        This method vacate target file if target file exist.
        :return: No return
        """
        FixtureFileHandler.vacate_target_if_exist(file_path)
        shutil.copy(str(file_path.resource), str(file_path.target))

    @staticmethod
    def restore_backup_if_exist(file_path: VacateFilePathInterface) -> NoReturn:
        """
        This method restore backup file by if exist.
        :return: No return
        """
        if file_path.backup.is_file():
            os.replace(str(file_path.backup), str(file_path.target))


class TargetFilePathVacator:
    """This class Vacate target file path."""
    FILE_PATH: VacateFilePathInterface
    @classmethod
    def setup(cls, file_path: VacateFilePathInterface = None) -> NoReturn:
        """This function vacate target if exist."""
        if file_path is None:
            file_path = cls.FILE_PATH
        FixtureFileHandler.vacate_target_if_exist(file_path)

    @classmethod
    def teardown(cls, file_path: VacateFilePathInterface = None) -> NoReturn:
        """This function restore backup if exist."""
        if file_path is None:
            file_path = cls.FILE_PATH
        FixtureFileHandler.restore_backup_if_exist(file_path)


class ResourceFileDeployer(TargetFilePathVacator):
    """This class Deploy resource file into target file path."""
    FILE_PATH: DeployFilePathInterface
    @classmethod
    def setup(cls, file_path: DeployFilePathInterface = None) -> NoReturn:
        """
        This method replace config file by file_path.resource.
        If file already exists, process backs up existing file.
        :return: No return
        """
        if file_path is None:
            file_path = cls.FILE_PATH
        FixtureFileHandler.deploy_resource(file_path)
