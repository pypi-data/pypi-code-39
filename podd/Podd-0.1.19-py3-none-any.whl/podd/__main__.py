"""Define the entry point when installing via pip."""

from podd.cli import cli_group
from podd.database import bootstrap_app


def podd():
    """Create main routine."""
    bootstrap_app()
    cli_group()


if __name__ == "__main__":
    podd()
