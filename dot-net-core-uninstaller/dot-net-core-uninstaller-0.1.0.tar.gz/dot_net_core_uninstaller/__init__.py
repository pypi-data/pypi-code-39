import logging
import platform
import shutil
import subprocess
import sys

import tabulate

__all__ = ["__version__", "Uninstaller"]

__version__ = '0.1.0'


class Uninstaller:
    """
    Removes the version .Net Core SDK and Runtime.
    """

    def __init__(self):

        if platform.system().lower() == 'windows':
            logging.error("Can only be used in posix systems.")
            sys.exit(1)

        try:
            dotnet_version = subprocess.check_output(["dotnet", "--version"]).strip()
            print(".Net Version found: {}".format(dotnet_version.decode('utf-8')))
        except FileNotFoundError as e:
            logging.error(".Net Core SDK is not installed")
            sys.exit(1)

    @staticmethod
    def _list_dotnet_sdks():
        dotnet_sdks = subprocess.check_output(["dotnet", "--list-sdks"]).decode('utf-8').split('\n')[:-1]

        return dotnet_sdks

    @staticmethod
    def _list_dotnet_runtimes():
        dotnet_runtimes = subprocess.check_output(["dotnet", "--list-runtimes"]).decode('utf-8').split('\n')[:-1]

        return dotnet_runtimes

    def convert_to_dict(self) -> dict:
        """
        Converts subprocess requests to dictionary.

        :return: A dictionary of version number with its path
        :rtype: dict
        """

        values = []
        for sdk in self._list_dotnet_sdks():
            sdk = sdk.split(' ')
            values.append([sdk[0], sdk[1][sdk[1].find("[") + 1: sdk[1].find("]")]])

        for runtime in self._list_dotnet_runtimes():
            runtime = runtime.split(' ')[1:]
            values.append([runtime[0], runtime[1][runtime[1].find("[") + 1: runtime[1].find("]")]])

        out = {}
        for key, val in values:
            out.setdefault(key, []).append(val + '/' + key)

        return out

    def delete(self, version_number: str):
        """
        Deletes the path of the given version, if available.

        :param str version_number: Version number of .Net Core SDK and Runtime to delete.
        """
        converted_dict = self.convert_to_dict()

        paths = converted_dict.get(version_number)

        if not paths:
            logging.error("Paths not found for .Net Core version {}.".format(version_number))
            sys.exit(1)

        print()
        print(tabulate.tabulate([[p] for p in paths], headers=["Deleting Version: {}".format(version_number)],
                                tablefmt="grid", colalign=("center",)))

        for path in paths:
            shutil.rmtree(path)

        print("Done.")

    def list_dotnet(self):
        """
        Lists all the installed .Net Core SDKs and Runtimes.
        """
        # TODO: this prints out both SDKs and Runtimes, need to separate them.
        paths = self.convert_to_dict()

        print()
        print(tabulate.tabulate([[p] for p in paths], headers=["List of .Net Core Versions Installed"],
                                tablefmt="grid", colalign=("center",)))
