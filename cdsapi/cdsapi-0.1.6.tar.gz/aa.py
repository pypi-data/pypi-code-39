#!/usr/bin/env python
import cdsapi
 
c = cdsapi.Client()
c.retrieve('reanalysis-era5-complete', {
"dataset":"era5",
"date":"2004-01-01",
"expver":"1",
"levtype":"ml",
"levelist":"2",
"param":"130",
"stream":"oper",
"class":"ea",
"time":"00:00:00/01:00:00",
"type":"an",       
}, 'data.grib')
