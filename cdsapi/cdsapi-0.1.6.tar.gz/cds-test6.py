#!/usr/bin/env python

# (C) Copyright 2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import cdsapi


c = cdsapi.Client(full_stack=True, url='https://cds-test.climate.copernicus.eu/api/v2',key='1:0698258a-5875-4a0a-b1be-57230eed83ca')

r = c.retrieve(
"satellite-albedo",
{
    "format": "zip", 
    "month": [
        "02", 
        "01"
    ], 
    "version": "1.5.1", 
    "year": [
        "2017", 
        "2015", 
        "2018", 
        "2016"
    ], 
    "variable": [
        "bi_hemispherical_albedo", 
        "directional_albedo", 
        "lai", 
        "fapar"
    ], 
    "day": "24"
}
)

r.download("x.grib")
