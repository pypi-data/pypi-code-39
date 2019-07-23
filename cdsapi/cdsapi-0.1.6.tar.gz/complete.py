
#!/usr/bin/env python

# (C) Copyright 2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import cdsapi

c = cdsapi.Client()

r  = c.retrieve("reanalysis-era5-complete",
{
'class': 'ea',
'stream': 'oper',
'date': '2016-01-01',
'levtype': 'sfc',
'param': '2t',
'grid':[0.25, 0.25],
'format': 'netcdf'

}
)

r.download("dowload.grib")

