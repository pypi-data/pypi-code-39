# File neme pattern:
# OR_ABI-L2–CMIPF–M3C09_G16_sYYYYJJJHHMMSSs_eYYYYJJJHHMMSSs_cYYYYJJJHHMMSSs.nc
# Where:
# OR: Operational System Real-Time Data
# ABI-L2: Advanced Baseline Imager Level 2+
# CMIPF: Cloud and Moisture Image Product – Full Disk
# M3 / M4: ABI Mode 3 or ABI Mode 4
# C09: Channel Number (Band 9 in this example)
# G16: GOES-16
# sYYYYJJJHHMMSSs: Observation Start
# eYYYYJJJHHMMSSs: Observation End
# cYYYYJJJHHMMSSs: File Creation


PRODUCT_TYPE = 'ABI-L2-CMIPF'
FILE_PATTERN = 'OR_ABI-L2-CMIPF-M3C{band:02d}_G16'
PATH_PREFIX = PRODUCT_TYPE + '/{year:04d}/{day_of_year:03d}/{hour:02d}/'


_prefix_pos = len(PATH_PREFIX.format(year=1111, day_of_year=11, hour=11)) + len(FILE_PATTERN.format(band=2)) + 2
SLICE_OBS_START = slice(_prefix_pos, _prefix_pos + len('20183650045364'))
