# -*- coding: utf-8 -*-
"""
Created on Wed May  9 15:12:14 2018

@author: MichaelEK
"""
import pytest
import xarray as xr
from nasadap import Nasa, parse_nasa_catalog
from time import time
import pandas as pd

pd.options.display.max_columns = 10

###############################
### Parameters

username = 'mullenkamp1' # Need to change for test
password = 'e8N5kxx8jYQvGYu' # Need to change for test
mission = 'gpm'
version = 6
product2d = '3IMERGHHE'
product2e = '3IMERGHHL'
product2f = '3IMERGHH'
from_date = '2019-05-01'
to_date = '2019-05-02'
dataset_type1 = 'precipitation'
dataset_type2 = 'precipitationCal'
min_lat=-49
max_lat=-33
min_lon=165
max_lon=180
cache_dir = r'\\fs02\GroundWaterMetData$\nasa\cache\nz'
cache_dir = ''

###############################
### Tests

## gpm


def test_gpm_session():
    ge = Nasa(username, password, mission)

    assert ge is not None

ge = Nasa(username, password, mission, cache_dir)


def test_gpm_dataset_types():
    ds_types = ge.get_dataset_types(product2d)

    assert ds_types is not None


def test_gpm_catalog():
    min_max1 = parse_nasa_catalog(mission, product2d, version, min_max=True)

    assert len(min_max1) > 2


def test_gpm4():
    ds2 = ge.get_data(product2d, version, dataset_type2, from_date, to_date, min_lat, max_lat, min_lon, max_lon)

    assert ds2[dataset_type2].shape == (96, 150, 160)


def test_gpm5():
    ds2 = ge.get_data(product2e, version, dataset_type2, from_date, to_date, min_lat, max_lat, min_lon, max_lon)

    assert ds2[dataset_type2].shape == (96, 150, 160)


def test_gpm6():
    ds2 = ge.get_data(product2f, version, dataset_type2, from_date, to_date, min_lat, max_lat, min_lon, max_lon)

    assert ds2[dataset_type2].shape == (96, 150, 160)

ge.close()
ds2.close()

#################################
### Other


#self = Nasa(username, password, mission)
#
#product = product2e
#dataset_types = dataset_type2
#dl_sim_count=30
#check_local=True
#missions = self.mission
#product = product2d
#from_date = '2019-06-01'
#to_date='2019-07-01'
#
#p1 = parse_nasa_catalog(mission, product, min_max=True)
#
#p2 = parse_nasa_catalog(mission, product, from_date=from_date, to_date=to_date)
#
#
#nc1 = r'E:\ecan\git\nasadap\nasadap\GPM_L3\GPM_3IMERGHHL.06\2019\182\3B-HHR-L.MS.MRG.3IMERG.20190701-S000000-E002959.0000.V06B.nc4'
#nc2 = r'E:\ecan\git\nasadap\nasadap\GPM_L3\GPM_3IMERGHHL.06\2019\182\*.nc4'
#
#ds1 = xr.open_mfdataset(nc2)

#hdf1 = 'https://disc2.gesdisc.eosdis.nasa.gov:443/opendap/TRMM_L3/TRMM_3B42.7/1998/002/3B42.19980102.03.7.HDF'
#nc1 = 'https://disc2.gesdisc.eosdis.nasa.gov:443/opendap/TRMM_L3/TRMM_3B42_Daily.7/1998/01/3B42_Daily.19980101.7.nc4'
#nc2 = 'https://gpm1.gesdisc.eosdis.nasa.gov/opendap/hyrax/GPM_L3/GPM_3IMERGDF.05/2014/03/3B-DAY.MS.MRG.3IMERG.20140312-S000000-E235959.V05.nc4'
#hdf2 = 'https://gpm1.gesdisc.eosdis.nasa.gov/opendap/hyrax/GPM_L3/GPM_3IMERGHH.05/2014/071/3B-HHR.MS.MRG.3IMERG.20140312-S000000-E002959.0000.V05B.HDF5'
#
#store = xr.backends.PydapDataStore.open(hdf1, session=ge.session)
#ds = xr.open_dataset(store)
#
#t1 = ds.attrs['FileHeader'].split(';\n')
#t2 = dict([t.split('=') for t in t1 if t != ''])

#ds3 = xr.Dataset(coords={'time': [], 'lat': [], 'lon': []})
#ds3 = xr.Dataset()
#
#ds3.to_netcdf(t1, unlimited_dims='time')
#
#ds3 = ds2.copy()
#
#ds3['time'] = ds3.time.to_series() + pd.DateOffset(days=2)
#
#with xr.open_mfdataset(t1) as ds:
#    print(ds)
##    ds4 = xr.concat([ds2, ds], dim='time')
#    ds4 = ds.combine_first(ds2)
#    ds5 = ds4.combine_first(ds3)
##    ds4 = xr.merge([ds, ds2])
##    ds5 = xr.merge([ds4, ds2])
#    print(ds5)
#
#ds4.to_netcdf(t1, mode='a', unlimited_dims='time')
#ds5.to_netcdf(t1, mode='a', unlimited_dims='time')

# ge = Nasa(username, password, mission1, cache_dir)
#
# start1 = time()
# ds1 = ge.get_data(product1a, dataset_type1, from_date, to_date, min_lat, max_lat, min_lon, max_lon, dl_sim_count=65)
# end1 = time()
#
# diff1 = end1 - start1


from nasadap import Nasa, parse_nasa_catalog

  ###############################
  ### Parameters

  mission = 'gpm'
  product = '3IMERGHH'
  version = 6
  from_date = '2019-03-28'
  to_date = '2019-03-29'
  dataset_type = 'precipitationCal'
  min_lat=-49
  max_lat=-33
  min_lon=165
  max_lon=180
  cache_dir = 'nasa/cache/nz'

  ###############################
  ### Examples

  min_max1 = parse_nasa_catalog(mission, product, version, min_max=True) # Will give you the min and max available dates for products

  ge1 = Nasa(username, password, mission, cache_dir)

  products = ge1.get_products()

  datasets = ge1.get_dataset_types(products[0])

  ds1 = ge1.get_data(product, version, dataset_type, from_date, to_date, min_lat, max_lat, min_lon, max_lon)
  ge1.close()
  ds1.close()

  from nasadap import agg

  ###############################
  ### Parameters

  cache_dir = 'nasa/cache/nz'
  save_dir = 'nasa/precip'

  username = '' # Need to change!
  password = '' # Need to change!

  mission = 'gpm'
  freq = 'M'
  product = '3IMERGHH'
  datasets = ['precipitationCal']

  min_lat=-49
  max_lat=-33
  min_lon=165
  max_lon=180
  dl_sim_count = 50
  tz_hour_gmt = 12

  time_combine(mission, product, version, datasets, save_dir, username, password, cache_dir, tz_hour_gmt, freq, min_lat, max_lat, min_lon, max_lon, dl_sim_count)







