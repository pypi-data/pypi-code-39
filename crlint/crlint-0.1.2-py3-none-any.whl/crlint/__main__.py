import argparse
import pathlib
import sys

from . import linting
from . import utils


def get_arguments() -> argparse.Namespace:
    """Parse user-provided CLI arguments.

    A user can change the default utility behavior.
    This method used to parse and prepare arguments.

    Returns:
        A parsed user-provided CLI arguments.
    """
    parser = argparse.ArgumentParser(description='Copyright linting utility')

    parser.add_argument(
        '-w',
        '--workdir',
        default=pathlib.Path.cwd(),
        help='Root directory to start copyrighting checking',
        type=pathlib.Path)

    return parser.parse_args()


def main() -> None:
    """Program entry point function."""
    try:
        arguments = get_arguments()
        config = utils.get_config(arguments.workdir)
        linting.lint_project(arguments.workdir, config.ignores)
    except Exception as e:
        sys.exit(e)


if __name__ == '__main__':
    main()
