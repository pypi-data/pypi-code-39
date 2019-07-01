import pathlib
import re
import typing

from . import exceptions
from . import utils


# Copyright re-strings template.
COPYRIGHT_TEMPLATE = [
    r"Copyright \(c\) 20\d{2} Celadon Development LLC, All rights reserved.",
    r"Author \w+ \w+ <\w+\.\w+@celadon.ae>",
]


def _build_copyright(copyright_lines: typing.List[str], comment_symbol: str) -> str:
    """Fill copyright template with comment symbols.

    For each language used in the project its own comment
    symbols. This method used to fill copyright string
    template with comment symbol for a specific language.

    Arguments:
        copyright_lines: a copyright strings template.
        comment_symbol: a symbol what used for commenting lines.

    Returns:
        A filled copyright template with comment symbol.
    """
    builded_copyright_lines = [
        ' '.join([comment_symbol, line])
        for line in copyright_lines
    ]
    return '\n'.join(builded_copyright_lines)


# Match file type with it is comment symbols by extension.
COPYRIGHT_BY_FILE_EXTENSION = {
    'js': _build_copyright(COPYRIGHT_TEMPLATE, '//'),
    'py': _build_copyright(COPYRIGHT_TEMPLATE, '#'),
    'yml': _build_copyright(COPYRIGHT_TEMPLATE, '#'),
}


def get_copyright_by_extension(file_path: str) -> str:
    """Get copyright by file extension.

    This method used to get the copyright string
    template for a specific language.

    Arguments:
        file_path: a file path to be inspected.

    Returns:
        A filled copytight re-string pattern.
    """
    extension = pathlib.Path(file_path).suffixes[-1].lstrip('.')
    return COPYRIGHT_BY_FILE_EXTENSION[extension]


def lint_file_copyright(file_path: str) -> None:
    """Check for file copyright and its status.

    All project files must contain a copyright stings.
    This method used to check the presence and status
    for copyright strings in the current file.

    Arguments:
        file_path: a path to file to be checked.

    Raises:
        CopyrightException: raises if file has broken copyright.
    """
    with pathlib.Path(file_path).open(encoding='utf-8') as file:
        file_copyright = re.compile(get_copyright_by_extension(file_path), re.MULTILINE)

        # Check copyright statements for a current file.
        if file_copyright.search(file.read()) is None:
            raise exceptions.CopyrightException(file_path)


def lint_project(work_path: pathlib.Path, exclusion: typing.List[str]) -> None:
    """Lint all files in the user-provided directory.

    This method used to check the copyright the presence
    and status for all files in user-provided project.

    Arguments:
        work_path: a root directory for running a check
        exclusion: exclusion file extension patterns.

    Raises:
        LinterException: raises if file has broken copyright.
    """
    problem_files = []
    for file_path in utils.scantree(work_path):
        if not utils.is_excluded(file_path, exclusion):
            try:
                lint_file_copyright(file_path)
            except exceptions.CopyrightException:
                problem_files.append(file_path)
            except Exception:
                pass

    # Show all broken files that have broken copyright.
    if problem_files:
        raise exceptions.CopyrightException(problem_files)
