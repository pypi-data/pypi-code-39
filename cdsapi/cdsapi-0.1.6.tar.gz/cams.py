#!/usr/bin/env python

# (C) Copyright 2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import cdsapi


c = cdsapi.Client(full_stack=True,
                  url='https://cams-dev.copernicus-atmosphere.eu/api/v2',
                  key='1:08c83f46-bd83-4a47-920a-18f26db65f51')

c.retrieve(
    'reanalysis-cams-pressure-levels',
    {
        'format': 'grib',
        'variable': [
            'geopotential', 'vertical_velocity'
        ],
        'pressure_level': '50',
        'year': '2003',
        'month': '08',
        'day': '20',
        'time': '00:00',
        'step': '0',
        'type': 'fc'
,'grid':'2/2'
    },
    'download.grib')
