#!/usr/bin/env python

# (C) Copyright 2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import cdsapi

c = cdsapi.Client(full_stack=True, url='https://cds-test.climate.copernicus.eu/api/v2',key='1:1c2ab50b-2208-4d84-b59d-87154cae4441')


r = c.retrieve(
    "reanalysis-era5-pressure-levels", {
    "day": "31", 
    "format": "netcdf", 
    "month": "02", 
    "pressure_level": [
      "500", 
      "550", 
      "600", 
      "650", 
      "700", 
      "750", 
      "775", 
      "800", 
      "825", 
      "850", 
      "875", 
      "900", 
      "925", 
      "950", 
      "975", 
      "1000"
    ], 
    "product_type": "reanalysis", 
    "time": [
      "00:00", 
      "01:00", 
      "02:00", 
      "03:00", 
      "04:00", 
      "05:00", 
      "06:00", 
      "07:00", 
      "08:00", 
      "09:00", 
      "10:00", 
      "11:00", 
      "12:00", 
      "13:00", 
      "14:00", 
      "15:00", 
      "16:00", 
      "17:00", 
      "18:00", 
      "19:00", 
      "20:00", 
      "21:00", 
      "22:00", 
      "23:00"
    ], 
    "variable": [
      "vertical_velocity"
    ], 
    "year": "2003"
  }
)

r.download("dowload.grib")
