from pkg_resources import get_distribution, DistributionNotFound
import re

__version_modifier__ = re.compile(r'^([0-9]+\.[0-9]+\.[0-9]+)\.(.*)$')
__distribution_name__ = 'reckoner_values'
try:
    __version__ = re.sub(__version_modifier__, r'\g<1>-\g<2>', get_distribution(__distribution_name__).version)
except DistributionNotFound:
    # Attempt to discover Version from pyinstaller data
    from pkgutil import get_data
    _raw_ver = get_data(__distribution_name__, 'version.txt').decode('UTF-8', 'ignore').rstrip("\r\n")
    __version__ = re.sub(__version_modifier__, r'\g<1>-\g<2>', _raw_ver)
__author__ = 'Croud Ltd'