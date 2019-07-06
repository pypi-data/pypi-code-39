# -*- coding: utf-8 -*-
"""
This module contains the unittests for the sptemp.analysis-module

Todo:
 
"""

import unittest
import datetime as dt
import os

import pyproj
import pandas as pd
import shapely.geometry as sg

from sptemp import zeit
from sptemp import moving_geometry as mg
from sptemp import analysis as aly
from sptemp.interpolation import ICollection as IC
from sptemp.interpolation import IPoint

direc = os.path.dirname(os.path.abspath(__file__))

class Test_SPT_DataFrame(unittest.TestCase):
    
    def setUp(self):
        
        self.tsu1 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.tsu2 = zeit.TS_Unit(IPoint.curve_point, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.ip1 = zeit.Interpolator([self.tsu1])
        self.ip2 = zeit.Interpolator([self.tsu2])
        
        self.ix = ["a","b","c","d","e"]
        self.id = [1,2,3,4,5]
        self.name = ["xy1","xy2","xy3","xy4","xy5"]
        self.temp = [zeit.Moving_Object([zeit.TS_Object(20.7, dt.datetime(2017, 07, 25, 20, 0, 0)), zeit.TS_Object(22.1, dt.datetime(2017, 07, 25, 20, 0, 10))], self.ip1),
                     zeit.Moving_Object([zeit.TS_Object(19.5, dt.datetime(2017, 07, 25, 20, 0, 2)), zeit.TS_Object(20.7, dt.datetime(2017, 07, 25, 20, 0, 20))], self.ip1),
                     zeit.Moving_Object([zeit.TS_Object(21.0, dt.datetime(2017, 07, 25, 20, 0, 1)), zeit.TS_Object(23.6, dt.datetime(2017, 07, 25, 20, 0, 10))], self.ip1),
                     zeit.Moving_Object([zeit.TS_Object(18.5, dt.datetime(2017, 07, 25, 20, 0, 0)), zeit.TS_Object(20.3, dt.datetime(2017, 07, 25, 20, 0, 20))], self.ip1),
                     zeit.Moving_Object([zeit.TS_Object(18.3, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 15)))], self.ip1)]
        
        self.geo1 = [sg.Point(11, 48), sg.Point(10, 48), sg.Point(11, 47), sg.Point(10, 47), sg.Point(11.5, 48.3)]
        
        self.geo2 = [mg.TS_Point(sg.Point(11, 48), dt.datetime(2017, 07, 25, 20, 0, 2)), mg.TS_Point(sg.Point(10, 48), dt.datetime(2017, 07, 25, 20, 0, 5)),
                     mg.TS_Point(sg.Point(11, 47), dt.datetime(2017, 07, 25, 20, 0, 4)), mg.TS_Point(sg.Point(10, 47), dt.datetime(2017, 07, 25, 20, 0, 10)),
                     mg.TS_Point(sg.Point(11.5, 48.3), zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 20)))]
        
        self.geo3 = [mg.Moving_Point([mg.TS_Point(sg.Point(3, 2), dt.datetime(2017, 07, 25, 20, 0, 20)),
                                      mg.TS_Point(sg.Point(4, 1), dt.datetime(2017, 07, 25, 20, 0, 30))], self.ip2)]
        
        self.c1 = sg.LineString([(3,2),(4,2),(4,1)])
        
    def test_init(self):
        
        # test if TypeError is raised if dataframe is not of type pandas.DataFrame
        with self.assertRaises(TypeError):
            aly.SPT_DataFrame({"id":self.id, "temp":self.temp, "geometry":self.geo1})
        
        # test if ValueError is raised if 'geometry' not in dataframe.columns
        with self.assertRaises(ValueError):
            aly.SPT_DataFrame(pd.DataFrame({"id":self.id, "temp":self.temp, "geo":self.geo1}))
            
        # test if TypeError is raised if crs is not of type pyproj.Proj
        with self.assertRaises(TypeError):
            aly.SPT_DataFrame(pd.DataFrame({"id":self.id, "temp":self.temp, "geometry":self.geo1}), crs=123)
            
        # test if TypeError is raised if geometry-column contains wrong type of objects
        with self.assertRaises(TypeError):
            aly.SPT_DataFrame(pd.DataFrame({"id":self.id, "temp":self.temp, "geometry":self.ix}))
            
        # test init
        spt_df = aly.SPT_DataFrame(pd.DataFrame({"id":self.id, "temp":self.temp, "geometry":self.geo1}, index=self.ix))
        self.assertEqual(spt_df.crs, None)
        #print spt_df.dataframe.loc["a"]["temp"].interpolate(dt.datetime(2017, 07, 25, 20, 0, 4)).value
    
    def test_geometry_type(self):
        
        spt_df = aly.SPT_DataFrame(pd.DataFrame({"id":self.id, "temp":self.temp, "geometry":self.geo1}))
        self.assertEqual(spt_df.geometry_type, sg.Point)
        
    def test_interpolate(self):
        
        spt_df1 = aly.SPT_DataFrame(pd.DataFrame({"id":self.id, "temp":self.temp, "geometry":self.geo1}, index=self.ix))
        spt_df1_t1 = spt_df1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 5))
        self.assertEqual(list(spt_df1_t1.dataframe.temp), [20.7, 19.5, 21, 18.5, 18.3])
        
        spt_df2 = aly.SPT_DataFrame(pd.DataFrame({"id":self.id, "temp":self.temp, "geometry":self.geo2}))
        spt_df2_t1 = spt_df2.interpolate(dt.datetime(2017, 07, 25, 20, 0, 5))
        self.assertEqual(list(spt_df2_t1.dataframe.temp), [19.5, 18.3])
        
        spt_df3 = aly.SPT_DataFrame(pd.DataFrame({"id":[1],
                                                  "temp":[zeit.Moving_Object([zeit.TS_Object(20.7, dt.datetime(2017, 07, 25, 20, 0, 0)), zeit.TS_Object(22.1, dt.datetime(2017, 07, 25, 20, 0, 10))], self.ip1)],
                                                  "geometry":self.geo3}, index=["a"]))
        
        arg_d = {"a":{"geometry":[self.c1]}}
        spt_df3_t2 = spt_df3.interpolate(dt.datetime(2017, 07, 25, 20, 0, 25), arg_d)
        self.assertEqual(spt_df3_t2.dataframe.loc["a"]["geometry"], sg.Point(4,2))
        
    def test_slice(self):
        
        spt_df1 = aly.SPT_DataFrame(pd.DataFrame({"id":self.id, "temp":self.temp, "geometry":self.geo1}, index=self.ix))
        spt_df1_s1 = spt_df1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 11), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.assertEqual(list(spt_df1_s1.dataframe["id"]), [1,2,3,4,5])
        self.assertEqual(spt_df1_s1.dataframe["temp"]["a"], None)
        
        spt_df2 = aly.SPT_DataFrame(pd.DataFrame({"id":self.id, "temp":self.temp, "geometry":self.geo2}))
        spt_df2_s1 = spt_df2.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.assertEqual(len(spt_df2_s1.dataframe), 2)
        self.assertEqual(spt_df2_s1.dataframe["geometry"][4].ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20)))
        
    def test_resampled_slice(self):
        
        spt_df1 = aly.SPT_DataFrame(pd.DataFrame({"id":self.id, "temp":self.temp, "geometry":self.geo1}, index=self.ix))
        spt_df1_s1 = spt_df1.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 11), dt.datetime(2017, 07, 25, 20, 0, 14), dt.datetime(2017, 07, 25, 20, 0, 20)])
        self.assertEqual(spt_df1_s1.dataframe["temp"]["a"], None)
        self.assertEqual(len(spt_df1_s1.dataframe["temp"]["b"]), 3)
        self.assertEqual(spt_df1_s1.dataframe["temp"]["b"].start_time(), dt.datetime(2017, 07, 25, 20, 0, 11))
        
        spt_df2 = aly.SPT_DataFrame(pd.DataFrame({"id":self.id, "temp":self.temp, "geometry":self.geo2}))
        spt_df2_s1 = spt_df2.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 14), dt.datetime(2017, 07, 25, 20, 0, 16)])
        self.assertEqual(len(spt_df2_s1.dataframe), 2)
        self.assertEqual(spt_df2_s1.dataframe["geometry"][4].start_time(), dt.datetime(2017, 07, 25, 20, 0, 10))
        self.assertEqual(spt_df2_s1.dataframe["geometry"][4].end_time(), dt.datetime(2017, 07, 25, 20, 0, 16))
        
    def test_reproject(self):
         
        spt_df1 = aly.SPT_DataFrame(pd.DataFrame({"id":self.id, "temp":self.temp, "geometry":self.geo1}, index=self.ix),crs=pyproj.Proj(init="epsg:4326"))
        spt_df1.reproject(pyproj.Proj(init="epsg:32631"))
        self.assertEqual(spt_df1.dataframe.geometry["a"], sg.Point(1096557.9347183318, 5347346.491066367))
         
        spt_df2 = aly.SPT_DataFrame(pd.DataFrame({"id":[1],
                                                  "geometry": [mg.TS_Point(sg.Point(11, 48), dt.datetime(2017, 07, 25, 20, 0, 10), crs=pyproj.Proj(init="epsg:4326"))]}))
         
        spt_df2.reproject(pyproj.Proj(init="epsg:32631"))
        self.assertEqual(spt_df2.dataframe.geometry[0].value, sg.Point(1096557.9347183318, 5347346.491066367))
        

unittest.main()  