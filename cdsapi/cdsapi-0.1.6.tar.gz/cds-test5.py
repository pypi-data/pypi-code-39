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
"satellite-sea-level-black-sea",
{
    "format": "zip", 
    "year": [
        "1996", 
        "2012", 
        "2000", 
        "2008", 
        "2004", 
        "2016"
    ], 
    "day": [
        "20", 
        "27", 
        "24", 
        "16", 
        "01", 
        "05", 
        "09", 
        "18", 
        "06", 
        "07", 
        "17", 
        "04", 
        "19", 
        "14", 
        "21", 
        "22", 
        "15", 
        "23", 
        "11", 
        "29", 
        "02", 
        "10", 
        "03", 
        "12", 
        "26", 
        "08", 
        "25", 
        "28", 
        "13"
    ], 
    "month": "02"
}
)

r.download("x.grib")
