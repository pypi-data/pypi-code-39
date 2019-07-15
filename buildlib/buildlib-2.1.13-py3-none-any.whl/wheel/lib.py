from typing import Optional
import shutil
import os
import glob
from cmdi import CmdResult, command, set_result, strip_args
import subprocess as sp

from .. import semver


def extract_version_from_wheel_name(name: str) -> str:
    """
    Get the version part out of the wheel file name.
    """
    parted: list = name.split('-')
    return '' if len(parted) < 2 else parted[1]


def find_wheel(
    wheel_dir: str,
    semver_num: Optional[str] = None,
    wheelver_num: Optional[str] = None,
    raise_not_found: Optional[bool] = False,
) -> Optional[str]:
    """
    Search dir for a wheel-file which contains a specific version number in its
    name. Return found wheel name or False.

    :param semver_num: Use a semver number to search for the wheel. This will convert the
    semver number into a wheel version number.
    :param wheelver_num: Use the exact version string that you see in the wheel file name to
    search for the wheel.
    """

    if wheelver_num:
        requested_version: str = wheelver_num

    elif semver_num:
        requested_version = semver.convert_semver_to_wheelver(semver_num)

    else:
        raise ValueError(
            'No version provided. Please provide either semver_num or '
            'wheelver_num.'
        )

    files: list = [file for file in os.listdir(wheel_dir)]

    matches: list = [
        file for file in files
        if extract_version_from_wheel_name(file) == requested_version
    ]

    if matches:
        return matches[0]

    elif not matches and raise_not_found:
        raise FileNotFoundError('Could not find wheel file.')

    else:
        return None


def push(
    wheel: str = 'dist/*',
    repository: str = 'pypi',
) -> None:
    """
    Push wheel file to registry via twine.
    """
    sp.run(['twine', 'upload', '-r', repository, wheel], check=True)


def build(cleanup: bool = False) -> None:
    """
    Build wheel.

    :param cleanup: Clean 'build' dir before running build command.
    """
    sp.run(
        ['python', 'setup.py', 'bdist_wheel'],
        check=True,
    )

    if cleanup:
        shutil.rmtree('./build', onerror=None)
        for f in glob.glob('**.egg-info'):
            shutil.rmtree(f)
