#!/usr/bin/env python

# (C) Copyright 2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import cdsapi


c = cdsapi.Client(full_stack=False, url='https://cds-test.climate.copernicus.eu/api/v2',key='1:0698258a-5875-4a0a-b1be-57230eed83ca')

r = c.retrieve(
    "reanalysis-era5-pressure-levels",
    {
       "variable": "t",
       "variable": "foobar",
       "pressure_level": "250",
       "product_type": "reanalysis",
       "date": "3017-12-01",
       "time": "12:00",
    },
)

r.download("x.grib")
