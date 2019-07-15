from settingscascade.manager import SettingsManager
from settingscascade.schema import ElementSchema

__all__ = ("SettingsManager", "ElementSchema")

try:
    import pkg_resources

    try:
        __version__ = pkg_resources.get_distribution("settingscascade").version
    except pkg_resources.DistributionNotFound:
        __version__ = "0.0.0"
except (ImportError, AttributeError):
    __version__ = "0.0.0"
