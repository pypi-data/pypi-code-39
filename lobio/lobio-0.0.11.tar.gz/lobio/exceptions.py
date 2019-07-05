class LoBioError(Exception):
    """Base exception for all lobio exceptions"""


class LoBioStrictError(LoBioError):
    """Exceptions raised for strictly invalid models"""


class StrictFeatureError(LoBioStrictError):
    """Exception if an invalid Feature is created"""


class RegionError(LoBioError):
    """Errors raised for invalid locations."""
