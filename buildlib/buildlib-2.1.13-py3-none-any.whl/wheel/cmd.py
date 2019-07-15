from typing import Optional
from cmdi import CmdResult, command, set_result, strip_args

from . import lib


@command
def push(
    wheel: str = 'dist/*',
    repository: str = 'pypi',
    **cmdargs,
) -> CmdResult:
    lib.push(**strip_args(locals()))
    return set_result()


@command
def build(
    cleanup: bool = False,
    **cmdargs,
) -> CmdResult:
    lib.build(**strip_args(locals()))
    return set_result()
