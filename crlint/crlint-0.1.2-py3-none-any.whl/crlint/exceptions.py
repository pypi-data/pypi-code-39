import typing


class LinterException(Exception):
    """The base exception class for all library raises."""


class CopyrightException(LinterException):
    """When the copyright of a file is in poor condition."""

    def __init__(self, errors: typing.Any) -> None:
        if isinstance(errors, (list, tuple)):
            # Convert pathlib.Path to list of objects for beautify print.
            errors = '\n '.join((str(error.absolute()) for error in errors))

        super().__init__('Failed linting in files:\n {0}'.format(errors))
