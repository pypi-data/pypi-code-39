#!/usr/bin/env python

# (C) Copyright 2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import cdsapi



c = cdsapi.Client(full_stack=True, url='https://cds-dev.copernicus-climate.eu/api/v2',key='1:66a653a6-4350-45c0-9e61-b6ca96e0e55a')



c.retrieve(
    'seasonal-original-single-levels',
    {
        'format':'grib',
        'originating_centre':'ecmwf',
        'system':'5',
        'variable':'2m_temperature',
        'year':'2014',
        'month':'07',
        'day':'01',
        'leadtime_hour':'24'
    },
    'download.grib')

