
#!/usr/bin/env python

# (C) Copyright 2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import cdsapi

c = cdsapi.Client(url="https://cds-test.climate.copernicus.eu/api/v2", key="1:6fb9050f-89e9-4683-bf6c-b2a13b27dd47")

r  = c.retrieve("satellite-carbon-dioxide", 
{
  "processing_level": "level_3",
  "variable": "xco2",
  "sensor_and_algorithm": "merged_obs4mips",
  "format": "tgz"
}
)

r.download("dowload.grib")

