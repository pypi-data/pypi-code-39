import os
import sys

from typing import Iterable, Callable

from .hash_observer import HashObserver
from .constants import EXCLUDE_RECOMMENDED


__all__ = [
    'observe',
]

TIP = """Observing path "{path}" triggering `{function}()` excluding:
"{excluded}".
"""


def observe(callback: Callable, path: str = '.', exclude: Iterable[str] = None):
    """Observe directory and trigger callback on change detection.

    :param callback: Target function to be called
    :param path: The observable root path
    :param exclude: Excluded files (default is tree_guardian.EXCLUDE_RECOMMENDED)
    """

    exclude = exclude or EXCLUDE_RECOMMENDED

    sys.stdout.write(TIP.format(
        path=os.path.abspath(path),
        function=callback.__name__,
        excluded='"; "'.join(exclude)
    ))
    sys.stdout.flush()

    observer = HashObserver(path=path, exclude=exclude)
    observer.observe(callback=callback)
