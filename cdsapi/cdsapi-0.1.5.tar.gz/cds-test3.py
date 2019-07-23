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
    "reanalysis-era5-single-levels", {
   "variable" : [
      "air_density_over_the_oceans",
      "charnock",
      "coefficient_of_drag_with_waves",
      "friction_velocity",
      "mean_direction_of_wind_waves",
      "mean_wave_direction",
      "mean_wave_period",
      "peak_wave_period",
      "significant_height_of_combined_wind_waves_and_swell",
      "u_component_stokes_drift",
      "v_component_stokes_drift"
   ],
   "time" : [
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
   "month" : "10",
   "area" : "52/-20/46/-10",
   "product_type" : "reanalysis",
   "format" : "netcdf",
   "day" : [
      "01",
      "02",
      "03",
      "04",
      "05",
      "06",
      "07",
      "08",
      "09",
      "10",
      "11",
      "12",
      "13",
      "14",
      "15",
      "16",
      "17",
      "18",
      "19",
      "20",
      "21",
      "22",
      "23",
      "24",
      "25",
      "26",
      "27",
      "28",
      "29",
      "30",
      "31"
   ],
   "year" : "2012"
}
)

r.download("x.grib")
