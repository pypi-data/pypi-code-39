"""Centralizes the enums used by the application"""

from enum import Enum

__all__ = ("StatusEnum",)


class StatusEnum(Enum):
    """Enum for mapping the status ids"""

    # Entities currently being processed
    PROCESSING = 1

    # Error status (and none of the previous execution succeeded)
    ERROR = 2

    # Success state
    UPDATED = 3

    # Error status (but at least one previous processing succeeded)
    OUTDATED = 4
