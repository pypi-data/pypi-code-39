# -*- coding: utf-8 -*-
"""
This module contains the unittests for the sptemp.interpolation-modul

Todo:
 
"""

import unittest
import datetime as dt

import shapely.geometry as sg
import pyproj

import sptemp.moving_geometry as mg
from sptemp import zeit
from sptemp.interpolation import ICollection as IC
from sptemp.interpolation import IPoint
from sptemp.interpolation import ICurve
from sptemp.interpolation import IRing
from sptemp.interpolation import I_Helper


class Test_ICollection(unittest.TestCase):
    
    def setUp(self):
        self.start_ts1 = zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 0))
        self.start_ts2 = zeit.TS_Object(10.0, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.start_ts3 = zeit.TS_Object("test", dt.datetime(2017, 07, 25, 20, 0, 0))
        
        self.end_ts1 = zeit.TS_Object(20, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.end_ts2 = zeit.TS_Object(20.0, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.end_ts3 = zeit.TS_Object("xy", dt.datetime(2017, 07, 25, 20, 0, 30))
        
    def test_undefined(self):
        
        t1 = dt.datetime(2017, 07, 25, 20, 0, 10)
        
        self.assertEqual(IC.undefined(self.start_ts1, self.end_ts1, t1), None)
        
    def test_constant(self):
        
        t1 = dt.datetime(2017, 07, 25, 20, 0, 10)
        
        self.assertEqual(IC.constant(self.start_ts1, self.end_ts1, t1), zeit.TS_Object(10, t1))
        
    def next_prev_ts(self):
        
        t1 = dt.datetime(2017, 07, 25, 20, 0, 10)
        
        self.assertEqual(IC.next_ts(self.start_ts1, self.end_ts1, t1), zeit.TS_Object(20, t1))
        
    def test_linear(self):
        
        # test if TypeError is raised if start_ts OR end_ts is not of type sptemp.zeit.TS_Object
        with self.assertRaises(TypeError):
            IC.linear(self.start_ts1, "xy", dt.datetime(2017, 07, 25, 20, 0, 10))
            
        with self.assertRaises(TypeError):
            IC.linear("xy", self.end_ts1, dt.datetime(2017, 07, 25, 20, 0, 10))
            
        # test if TypeError is raised if time is not of type datetime.datetime
        with self.assertRaises(TypeError):
            IC.linear(self.start_ts1, self.end_ts1, "xy")
            
        # test if ValueError is raised if start_ts.type != end_ts.type
        with self.assertRaises(ValueError):
            IC.linear(self.start_ts1, self.end_ts2, dt.datetime(2017, 07, 25, 20, 0, 10))
            
        # test if ValueError is raised if start_ts.end_time() > end_ts.start_time()
        with self.assertRaises(ValueError):
            IC.linear(self.end_ts1, self.start_ts1, dt.datetime(2017, 07, 25, 20, 0, 10))
            
        t1 = dt.datetime(2017, 07, 25, 20, 0, 12)
        t2 = dt.datetime(2017, 07, 25, 20, 0, 10)
        t3 = dt.datetime(2017, 07, 25, 20, 0, 20)
        t4 = dt.datetime(2017, 07, 25, 20, 0, 12, 111)
        
        self.assertEqual(IC.linear(self.start_ts1, self.end_ts1, t1), zeit.TS_Object(16, t1))
        self.assertEqual(IC.linear(self.start_ts1, self.end_ts1, t2), zeit.TS_Object(15, t2))
        self.assertEqual(IC.linear(self.start_ts1, self.end_ts1, t3), zeit.TS_Object(20, t3))
        self.assertEqual(IC.linear(self.start_ts1, self.end_ts1, t4), zeit.TS_Object(16, t4))
        
        self.assertEqual(IC.linear(self.start_ts2, self.end_ts2, t1), zeit.TS_Object(12.0, t1))
        self.assertEqual(IC.linear(self.start_ts2, self.end_ts2, t2), zeit.TS_Object(10.0, t2))
        self.assertEqual(IC.linear(self.start_ts2, self.end_ts2, t3), zeit.TS_Object(20.0, t3))
        self.assertEqual(IC.linear(self.start_ts2, self.end_ts2, t4), zeit.TS_Object(12.000111, t4))


class Test_IPoint(unittest.TestCase):
    
    def setUp(self):
        self.tsp1 = mg.TS_Point(sg.Point(1, 2, 460), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tsp2 = mg.TS_Point(sg.Point(3, 1, 470), zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20)))
        
        self.tsp3 = mg.TS_Point(sg.Point(1, 2), zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.tsp4 = mg.TS_Point(sg.Point(3, 1), zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        
    def test_linear_point(self):
        
        # test if TypeError is raised if ts_start or ts_end is not of type sptemp.moving_object.TS_Point
        with self.assertRaises(TypeError):
            IPoint.linear_point(zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 0)), self.tsp2, dt.datetime(2017, 07, 25, 20, 0, 2))
            
        with self.assertRaises(TypeError):
            IPoint.linear_point(self.tsp1, zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 10)), dt.datetime(2017, 07, 25, 20, 0, 2))
            
        # test if TypeError is raised if time is not of type datetime.datetime
        with self.assertRaises(TypeError):
            IPoint.linear_point(self.tsp1, self.tsp2, 123)
            
        # test if ValueError is raised if start_ts.has_z != end_ts.has_z
        with self.assertRaises(ValueError):
            IPoint.linear_point(self.tsp1, self.tsp4, dt.datetime(2017, 07, 25, 20, 0, 2))
            
        # test if Value Error is raised if start_ts.end_time() >= end_ts.start_time()
        with self.assertRaises(ValueError):
            IPoint.linear_point(self.tsp2, self.tsp1, dt.datetime(2017, 07, 25, 20, 0, 2))
            
        # test if Value Error is raised if time < start_ts.end_time() OR time > end_ts.start_time()
        with self.assertRaises(ValueError):
            IPoint.linear_point(self.tsp1, self.tsp2, dt.datetime(2017, 07, 25, 19, 0, 2))
            
        with self.assertRaises(ValueError):
            IPoint.linear_point(self.tsp1, self.tsp2, dt.datetime(2017, 07, 25, 19, 0, 11))
            
        # test if ValueError is raised if start_ts.crs != end_ts.crs
        with self.assertRaises(ValueError):
            IPoint.linear_point(mg.TS_Point(sg.Point(1, 2), dt.datetime(2017, 07, 25, 20, 0, 10)),
                                mg.TS_Point(sg.Point(2, 2), dt.datetime(2017, 07, 25, 20, 0, 20), pyproj.Proj(init="epsg:32631")),
                                dt.datetime(2017, 07, 25, 19, 0, 11))
            
        with self.assertRaises(ValueError):
            IPoint.linear_point(mg.TS_Point(sg.Point(1, 2), dt.datetime(2017, 07, 25, 20, 0, 10), pyproj.Proj(init="epsg:4326")),
                                mg.TS_Point(sg.Point(2, 2), dt.datetime(2017, 07, 25, 20, 0, 20), pyproj.Proj(init="epsg:32631")),
                                dt.datetime(2017, 07, 25, 19, 0, 11))
        
        
        
        t1 = dt.datetime(2017, 07, 25, 20, 0, 5)
        t2 = dt.datetime(2017, 07, 25, 20, 0, 7)
        t3 = dt.datetime(2017, 07, 25, 20, 0, 13)
        t4 = dt.datetime(2017, 07, 25, 20, 0, 18, 111)
        
        # test if correct values are returned
        self.assertEqual(IPoint.linear_point(self.tsp1, self.tsp2, t1), mg.TS_Point(sg.Point(2, 1.5, 465), t1))
        self.assertEqual(IPoint.linear_point(self.tsp1, self.tsp2, t2), mg.TS_Point(sg.Point(2.3999999999999995, 1.3, 467.0), t2))
        self.assertEqual(IPoint.linear_point(self.tsp3, self.tsp4, t3), mg.TS_Point(sg.Point(1.5999999999999999, 1.7), t3))
        self.assertEqual(IPoint.linear_point(self.tsp3, self.tsp4, t4), mg.TS_Point(sg.Point(2.6000222000000006, 1.1999889), t4))
        
    def test_curve_point(self):
        
        tsp1 = mg.TS_Point(sg.Point(1, 1), dt.datetime(2017, 07, 25, 20, 0, 0))
        tsp2 = mg.TS_Point(sg.Point(5, 2), dt.datetime(2017, 07, 25, 20, 0, 20))
        
        tsp3 = mg.TS_Point(sg.Point(100, 100, 490), dt.datetime(2017, 07, 25, 20, 0, 0))
        tsp4 = mg.TS_Point(sg.Point(500, 200, 500), dt.datetime(2017, 07, 25, 20, 0, 20))
        
        c1 = sg.LineString([(1,1), (3,1), (3,2), (5,2)])
        c2 = sg.LineString([(100,100,490), (300,100,490), (300,200,500), (500,200,500)])
        
        t1 = dt.datetime(2017, 07, 25, 20, 0, 0)
        t2 = dt.datetime(2017, 07, 25, 20, 0, 2)
        t3 = dt.datetime(2017, 07, 25, 20, 0, 8)
        t4 = dt.datetime(2017, 07, 25, 20, 0, 10)
        t5 = dt.datetime(2017, 07, 25, 20, 0, 16)
        t6 = dt.datetime(2017, 07, 25, 20, 0, 20)
        
        # test start_ts or end_ts is not of type sptemp.moving_geometry.TS_Point
        with self.assertRaises(TypeError):
            IPoint.curve_point(zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 0)), tsp2, dt.datetime(2017, 07, 25, 20, 0, 2), c1)
            
        with self.assertRaises(TypeError):
            IPoint.curve_point(tsp1, zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 10)), dt.datetime(2017, 07, 25, 20, 0, 2), c1)
            
        # test if TypeError is raised if time is not of type datetime.datetime
        with self.assertRaises(TypeError):
            IPoint.curve_point(tsp1, tsp2, 123, c1)
            
        # test if TypeError is raised if curve is not of type shapely.geometry.LineString
        with self.assertRaises(TypeError):
            IPoint.curve_point(tsp1, tsp2, t1, sg.Point(1, 1))
            
        # test if ValueError is raised if start_ts.has_z, end_ts.has_z and curve.has_z is not equal
        with self.assertRaises(ValueError):
            IPoint.curve_point(tsp1, tsp4, t1, c1)
            
        with self.assertRaises(ValueError):
            IPoint.curve_point(tsp1, tsp2, t1, c2)
            
        # test if ValueError is raised if start_ts.crs != end_ts.crs
        with self.assertRaises(ValueError):
            IPoint.curve_point(tsp1, mg.TS_Point(sg.Point(5, 2), dt.datetime(2017, 07, 25, 20, 0, 20), pyproj.Proj(init="epsg:32631")), t1, c1)
            
        with self.assertRaises(ValueError):
            IPoint.curve_point(mg.TS_Point(sg.Point(1, 1), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326")),
                               mg.TS_Point(sg.Point(5, 2), dt.datetime(2017, 07, 25, 20, 0, 20), pyproj.Proj(init="epsg:32631")), t1, c1)
            
        # test if ValueError is raised if start_ts.end_time >= end_ts.start_time()
        with self.assertRaises(ValueError):
            IPoint.curve_point(tsp2, tsp1, t1, c1)
            
        # test if ValueError is raised if time < start_ts.end_time() OR time < send_ts.start_time()
        with self.assertRaises(ValueError):
            IPoint.curve_point(tsp1, tsp2, dt.datetime(2017, 07, 25, 19, 0, 20), c1)
            
        with self.assertRaises(ValueError):
            IPoint.curve_point(tsp1, tsp2, dt.datetime(2017, 07, 25, 20, 0, 21), c1)
            
        # test if ValueError is raised if start_ts.value does not equal start point of curve 
        # OR if end_ts.value does not equal end point of curve
        with self.assertRaises(ValueError):
            IPoint.curve_point(tsp3, tsp4, t1, sg.LineString([(1,1,490), (3,1,490), (3,2,500), (5,2,500)]))
        
        # test if correctly interpolated value is returned
        # without z-coordinate
        self.assertEqual(IPoint.curve_point(tsp1, tsp2, t1, c1), mg.TS_Point(sg.Point(1,1), t1))
        self.assertEqual(IPoint.curve_point(tsp1, tsp2, t2, c1), mg.TS_Point(sg.Point(1.5,1), t2))
        self.assertEqual(IPoint.curve_point(tsp1, tsp2, t3, c1), mg.TS_Point(sg.Point(3,1), t3))
        self.assertEqual(IPoint.curve_point(tsp1, tsp2, t4, c1), mg.TS_Point(sg.Point(3,1.5), t4))
        self.assertEqual(IPoint.curve_point(tsp1, tsp2, t5, c1), mg.TS_Point(sg.Point(4,2), t5))
        self.assertEqual(IPoint.curve_point(tsp1, tsp2, t6, c1), mg.TS_Point(sg.Point(5,2), t6))
        
        # with z-coordinate
        self.assertEqual(IPoint.curve_point(tsp3, tsp4, t1, c2), mg.TS_Point(sg.Point(100,100,490), t1))
        self.assertEqual(IPoint.curve_point(tsp3, tsp4, t2, c2), mg.TS_Point(sg.Point(150.04987562,100,490), t2))
        self.assertEqual(IPoint.curve_point(tsp3, tsp4, t3, c2), mg.TS_Point(sg.Point(300,100.19851239,490.01985124), t3))
        self.assertEqual(IPoint.curve_point(tsp3, tsp4, t4, c2), mg.TS_Point(sg.Point(300,150,495), t4))
        self.assertEqual(IPoint.curve_point(tsp3, tsp4, t5, c2), mg.TS_Point(sg.Point(399.90024876,200,500), t5))
        self.assertEqual(IPoint.curve_point(tsp3, tsp4, t6, c2), mg.TS_Point(sg.Point(500,200,500), t6))
        
    
class Test_ICurve(unittest.TestCase):
        
    def setUp(self):
            
        self.tsl1 = mg.TS_LineString(sg.LineString([(2,0),(1,1),(1.5,2),(2.5,2.5),(2.5,3.5)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tsl2 = mg.TS_LineString(sg.LineString([(5.5,0),(5,1),(6,2.5)]), dt.datetime(2017, 07, 25, 20, 0, 10))
        self.tsl3 = mg.TS_LineString(sg.LineString([(7,0),(7,1),(8,1.5),(9,3)]), dt.datetime(2017, 07, 25, 20, 0, 20))
        self.tsl3_1 = mg.TS_LineString(sg.LineString([(7,0),(7,1),(8,0.5),(8,1.5),(8.5,2),(9,3)]), dt.datetime(2017, 07, 25, 20, 0, 30))
        
        self.tsl4 = mg.TS_LineString(sg.LineString([(2,0,3),(1,1,3),(1.5,2,2),(2.5,2.5,3),(2.5,3.5,2)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tsl5 = mg.TS_LineString(sg.LineString([(5.5,0,2),(5,1,3),(6,2.5,2)]), dt.datetime(2017, 07, 25, 20, 0, 10))
            
        self.t1 = dt.datetime(2017, 07, 25, 20, 0, 5)
        self.t2 = dt.datetime(2017, 07, 25, 20, 0, 15)
        self.t3 = dt.datetime(2017, 07, 25, 20, 0, 25)
            
    def test_basic_linear(self):
        
        # test if TypeError is raised if start_ts or end_ts not of type sptemp.moving_geometry.TS_LineString
        with self.assertRaises(TypeError):
            ICurve.basic_linear(mg.TS_Point(sg.Point(1, 1), dt.datetime(2017, 07, 25, 20, 0, 0)), self.tsl2, self.t1)
            
        with self.assertRaises(TypeError):
            ICurve.basic_linear(self.tsl1, mg.TS_Point(sg.Point(3, 1), dt.datetime(2017, 07, 25, 20, 0, 20)), self.t1)
            
        
        # test if TypeError is raised if type of time is not datetime.datetime
        with self.assertRaises(TypeError):
            ICurve.basic_linear(self.tsl1, self.tsl2, 123)
            
        # test if ValueError is raised if start_ts.has_z != end_ts.has_z
        with self.assertRaises(ValueError):
            ICurve.basic_linear(mg.TS_LineString(sg.LineString([(5.5,0,4),(5,1,3),(6,2.5,2)]), dt.datetime(2017, 07, 25, 20, 0, 10)),
                                mg.TS_LineString(sg.LineString([(7,0),(7,1),(8,1.5),(9,3)]), dt.datetime(2017, 07, 25, 20, 0, 20)), self.t2)
            
        # test if start_ts.crs != end_ts.crs
        with self.assertRaises(ValueError):
            ICurve.basic_linear(mg.TS_LineString(sg.LineString([(5.5,0),(5,1),(6,2.5)]), dt.datetime(2017, 07, 25, 20, 0, 10), pyproj.Proj(init="epsg:32631")),
                                mg.TS_LineString(sg.LineString([(7,0),(7,1),(8,1.5),(9,3)]), dt.datetime(2017, 07, 25, 20, 0, 20)), self.t2)
            
        with self.assertRaises(ValueError):
            ICurve.basic_linear(mg.TS_LineString(sg.LineString([(5.5,0),(5,1),(6,2.5)]), dt.datetime(2017, 07, 25, 20, 0, 10), pyproj.Proj(init="epsg:32631")),
                                mg.TS_LineString(sg.LineString([(7,0),(7,1),(8,1.5),(9,3)]), dt.datetime(2017, 07, 25, 20, 0, 20), pyproj.Proj(init="epsg:4326")),
                                self.t2)
            
        # test if ValueError is raised if start_ts.end_time() >= end_ts.start_time()
        with self.assertRaises(ValueError):
            ICurve.basic_linear(self.tsl2, self.tsl1, self.t1)
            
        # test if valueError is raised if time < start_ts.end_time() or time > end_ts.start_time()
        with self.assertRaises(ValueError):
            ICurve.basic_linear(self.tsl1, self.tsl2, self.t2)
            
        with self.assertRaises(ValueError):
            ICurve.basic_linear(self.tsl2, self.tsl3, self.t1)
                            
        # test if correct values are returned
        self.assertEqual(ICurve.basic_linear(self.tsl1, self.tsl2, self.t1),
                         mg.TS_LineString(sg.LineString([(3.75, 0.0), (3.0, 1.0), (3.4227457514062634, 1.7591186271093946),
                                                         (4.095491502812527, 2.268237254218789), (4.25, 3.0)]), self.t1))
        
        self.assertEqual(ICurve.basic_linear(self.tsl2, self.tsl3, self.t2),
                         mg.TS_LineString(sg.LineString([(6.25, 0.0), (6.0, 1.0), (6.691391109268659, 1.537086663902989), (7.5, 2.75)]),self.t2))
        
        self.assertEqual(ICurve.basic_linear(self.tsl2, self.tsl3, self.t2, "distance"),
                         mg.TS_LineString(sg.LineString([(6.25, 0.0), (6.0, 1.0), (6.691391109268659, 1.537086663902989), (7.5, 2.75)]),self.t2))
        
        self.assertEqual(ICurve.basic_linear(self.tsl4, self.tsl5, self.t1, "distance"),
                         mg.TS_LineString(sg.LineString([(3.75, 0.0, 2.5), (3.0, 1.0, 3.0), (3.4227457514062634, 1.7591186271093946, 2.3272542485937366),
                                                         (4.095491502812527, 2.268237254218789, 2.6545084971874737), (4.25, 3.0, 2.0)]),self.t1))
        
    
class Test_IRing(unittest.TestCase):
    
    def setUp(self):
        
        self.tslr1 = mg.TS_LinearRing(sg.LinearRing([(1,1),(2,1),(2,2),(1,2),(1,1)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tslr2 = mg.TS_LinearRing(sg.LinearRing([(3,1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 10))
        
        self.t1 = dt.datetime(2017, 07, 25, 20, 0, 5)
        
    def test_linear_translation(self):
        
        # test if TypeError is raised if start_ts or end_ts not of type sptemp.moving_geometry.TS_LinearRing
        with self.assertRaises(TypeError):
            IRing.linear_translation(mg.TS_LineString(sg.LineString([(1,1),(2,1),(2,2),(1,2),(1,1)]), dt.datetime(2017, 07, 25, 20, 0, 0)), self.tslr2, self.t1)
            
        with self.assertRaises(TypeError):
            IRing.linear_translation(self.tslr1, mg.TS_LineString(sg.LineString([(3,1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 10)), self.t1)
            
        
        # test if TypeError is raised if type of time is not datetime.datetime
        with self.assertRaises(TypeError):
            IRing.linear_translation(self.tslr1, self.tslr2, 123)
            
        # test if ValueError is raised if start_ts.has_z != end_ts.has_z
        with self.assertRaises(ValueError):
            IRing.linear_translation(self.tslr1,
                                     mg.TS_LinearRing(sg.LinearRing([(3,1,2),(4,1,3),(4,2,2),(3,2,2),(3,1,2)]), dt.datetime(2017, 07, 25, 20, 0, 10)), self.t1)
            
        # test if start_ts.crs != end_ts.crs
        with self.assertRaises(ValueError):
            IRing.linear_translation(self.tslr1,
                                     mg.TS_LinearRing(sg.LinearRing([(3,1),(4,1),(4,2),(3,2),(3,1)]),
                                                      dt.datetime(2017, 07, 25, 20, 0, 10), pyproj.Proj(init="epsg:32631")),
                                     self.t1)
            
        with self.assertRaises(ValueError):
            IRing.linear_translation(mg.TS_LinearRing(sg.LinearRing([(1,1),(2,1),(2,2),(1,2),(1,1)]),
                                                      dt.datetime(2017, 07, 25, 20, 0, 10), pyproj.Proj(init="epsg:4326")),
                                                      mg.TS_LinearRing(sg.LinearRing([(3,1),(4,1),(4,2),(3,2),(3,1)]),
                                                                       dt.datetime(2017, 07, 25, 20, 0, 10), pyproj.Proj(init="epsg:32631")),
                                                      self.t1)
            
        # test if ValueError is raised if start_ts.end_time() >= end_ts.start_time()
        with self.assertRaises(ValueError):
            IRing.linear_translation(self.tslr2, self.tslr1, self.t1)
            
        # test if valueError is raised if time < start_ts.end_time() or time > end_ts.start_time()
        with self.assertRaises(ValueError):
            IRing.linear_translation(self.tslr1, self.tslr2, dt.datetime(2017, 07, 25, 20, 0, 20))
            
        with self.assertRaises(ValueError):
            IRing.linear_translation(self.tslr1, self.tslr2, dt.datetime(2017, 07, 25, 19, 0, 20))
            
        # test if value id interpolated correctly
        tlr_t1 = IRing.linear_translation(self.tslr1, self.tslr2, self.t1)
        self.assertEqual(tlr_t1, mg.TS_LinearRing(sg.LinearRing([(2,1),(3,1),(3,2),(2,2),(2,1)]), self.t1))
        
    def test_basic_linear(self):
        
        ts_lr1 = mg.TS_LinearRing(sg.LinearRing([(1,0.5),(2.25,0.75),(1.5,1.25),(1.75,1.75),(1.25,2.25),(0.5,1.75),(0.5,1.0),(1,0.5)]),
                                  dt.datetime(2017, 07, 25, 20, 0, 0))
        ts_lr2 = mg.TS_LinearRing(sg.LinearRing([(3.0,0.5),(4.5,0.5),(3.75,2.25),(3.0,0.5)]),
                                  dt.datetime(2017, 07, 25, 20, 0, 20))
        
        ts_lr3 = mg.TS_LinearRing(sg.LinearRing([(1,1),(1.25,1.75),(1.5,1.75),(1.5,1.25),(2,1),(2,2),(1.75,1.75),(1,2),(1,1)]),
                                  dt.datetime(2017, 07, 25, 20, 0, 0))
        ts_lr4 = mg.TS_LinearRing(sg.LinearRing([(4.5,1.5),(4,2),(3.5,1.5),(3.5,0.5),(3.75,1.25),(4,1.25),(4,1),(4.5,1),(4.25,1.25),(4.5,1.5)]),
                                  dt.datetime(2017, 07, 25, 20, 0, 20))
        
        self.assertEqual(IRing.basic_linear(ts_lr1, ts_lr2, dt.datetime(2017, 07, 25, 20, 0, 10)).value.coords[:],
                         [(3.375, 0.625), (2.8440513845721638, 1.2388801026649512), (2.872336158951433, 1.7145489624466568),
                          (2.5, 2.25), (1.9816795819387427, 1.6655856911903992), (1.8624297859062504, 1.0123361671145843), (2.0, 0.5), (3.375, 0.625)])
        
        self.assertEqual(IRing.basic_linear(ts_lr3, ts_lr4, dt.datetime(2017, 07, 25, 20, 0, 10)).value.coords[:],
                         [(3.25, 1.0), (3.125, 1.625), (3.125, 1.625), (2.5, 2.0), (2.25, 1.5428932188134525),
                          (2.25, 0.75), (2.5, 1.5), (2.75, 1.5), (2.75, 1.125), (3.25, 1.0)])
        
        self.assertEqual(IRing.basic_linear(ts_lr1, ts_lr2, dt.datetime(2017, 07, 25, 20, 0, 10), "distance").value.coords[:],
                         [(3.375, 0.625), (2.8440513845721638, 1.2388801026649512), (2.872336158951433, 1.7145489624466568), (2.5, 2.25),
                          (1.9816795819387427, 1.6655856911903992), (1.8624297859062504, 1.0123361671145843), (2.0, 0.5), (3.375, 0.625)])
        
        
class Test_IHelper(unittest.TestCase):
    
    def angle(self):
        
        self.assertEqual(I_Helper.angle((2,1),(1,1),(1.25,1.25)), 45)
        self.assertEqual(I_Helper.angle((5,1),(6,2),(7,3)), 0)
    
    def test_angle_to_x_axis(self):
        
        self.assertEqual(I_Helper.angle_to_x_axis((1,1),(1.25,1.25)), 45.0)
        self.assertEqual(I_Helper.angle_to_x_axis((1,1),(2,1)), 0.0)
        self.assertEqual(I_Helper.angle_to_x_axis((1,1),(1,2)), 90.0)
        self.assertEqual(I_Helper.angle_to_x_axis((1,1),(0,1)), 180.0)
        self.assertEqual(I_Helper.angle_to_x_axis((1,1),(1,0)), 270.0)
    
    def test_curve_segments(self):
        
        lr = sg.LinearRing([(1,1),(2,1),(2,2),(1,2),(1,1)])
        lr_seg = I_Helper.curve_segments(lr)
        
        self.assertEqual(lr_seg, [[(1.0, 1.0), (2.0, 1.0)], [(2.0, 1.0), (2.0, 2.0)], [(2.0, 2.0), (1.0, 2.0)], [(1.0, 2.0), (1.0, 1.0)]])
        
    def test_linestring_from_segments(self):
        
        lr_seg = [[(1.0, 1.0), (2.0, 1.0)], [(2.0, 1.0), (3.0, 1.5), (2.0, 2.0)], [(2.0, 2.0), (1.0, 2.0)], [(1.0, 2.0), (1.0, 1.0)]]
        lr = I_Helper.linestring_from_segments(lr_seg)
        self.assertEqual(lr.coords[:], [(1.0, 1.0), (2.0, 1.0), (3.0, 1.5), (2.0, 2.0), (1.0, 2.0), (1.0, 1.0)])
            
    def test_create_diff_dict(self):
        
        lr = sg.LinearRing([(1.5,1.5),(2,1),(2,2),(1,2),(1,1),(1.5,1.5)])
        lr_convex = sg.LinearRing(lr.convex_hull.exterior.coords[::-1])
        
        lr_seg = I_Helper.curve_segments(lr)
        lr_convex_seg = I_Helper.curve_segments(lr_convex)
        
        d_dict = I_Helper.create_diff_dict(lr_convex_seg, lr_seg)
        self.assertEqual(d_dict, {0: [(1.0, 1.0), (1.5, 1.5), (2.0, 1.0)]})
        
    def test_basic_simpify(self):
        lr = [(0.5,1.0),(1.0,0.5),(1.5,1.0),(1.5,2.0),(0.5,2.5),(0.5,3.0),(1.0,3.5)]
           

unittest.main()                               