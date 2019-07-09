# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Enable consuming Azure open datasets into dataframes and enrich customer data."""

from ._boston_safety import BostonSafety
from ._chicago_safety import ChicagoSafety
from ._noaa_gfs_weather import NoaaGfsWeather
from ._noaa_isd_weather import NoaaIsdWeather
from ._nyc_safety import NycSafety
from ._nyc_tlc_fhv import NycTlcFhv
from ._nyc_tlc_green import NycTlcGreen
from ._nyc_tlc_yellow import NycTlcYellow
from ._public_holidays import PublicHolidays
from ._sanfrancisco_safety import SanFranciscoSafety
from ._seattle_safety import SeattleSafety

__all__ = [
    'BostonSafety',
    'ChicagoSafety',
    'NoaaGfsWeather',
    'NoaaIsdWeather',
    'NycSafety',
    'NycTlcFhv',
    'NycTlcGreen',
    'NycTlcYellow',
    'PublicHolidays',
    'SanFranciscoSafety',
    'SeattleSafety'
]
