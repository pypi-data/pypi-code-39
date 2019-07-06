# -*- coding: utf-8 -*-
"""
This module contains the unittests for the sptemp.moving_geometry-modul

Todo:
 
"""
import unittest
import datetime as dt

import pyproj
import shapely.geometry as sg

from sptemp import moving_geometry as mg
from sptemp import zeit
from sptemp.interpolation import ICollection as IC
from sptemp.interpolation import IPoint
from sptemp.interpolation import ICurve
from sptemp.interpolation import IRing


class Test_TS_Geometry(unittest.TestCase):
    
    def setUp(self):
        self.tsg1 = mg.TS_Geometry(sg.Point(10.2, 2.4, 460), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tsg2 = mg.TS_Geometry(sg.Point(12.2, 10.4), zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 10)))
        
    def test_init(self):
        
        # test if TypeError is raised if value not of type shapely.geometry
        with self.assertRaises(TypeError):
            mg.TS_Geometry(123, dt.datetime(2017, 07, 25, 20, 0, 0))
            
        # test if ValueError is raised if shapely.geometry is empty
        with self.assertRaises(ValueError):
            mg.TS_Geometry(sg.Point(), dt.datetime(2017, 07, 25, 20, 0, 0))
                
        # test if TypeError is raised when ts is not of type datetime.datetime and ts is not of type Time_Period
        with self.assertRaises(TypeError):
            mg.TS_Geometry(sg.Point(10.2, 2.4, 460), 123)
            
        # test if TypeError is raised if crs is not of type pyproj.Proj
        with self.assertRaises(TypeError):
            mg.TS_Geometry(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0), 123)
            
    def test_value(self):
        
        # test if correct value is returned
        self.assertEqual(self.tsg1.value, sg.Point(10.2, 2.4, 460))
        
        # test if TypeError is raised if assigned value is not of same type
        with self.assertRaises(TypeError):
            self.tsg1.value = sg.LineString([(1,2),(3,2)])
            
        # test if ValueError is raised if self.has_z != value.has_z
        with self.assertRaises(ValueError):
            self.tsg1.value = sg.Point(11.4, 4.5)
            
        with self.assertRaises(ValueError):
            self.tsg2.value = sg.Point(11.4, 4.5, 500)
            
        # test if correct value is assigned
        self.tsg1.value = sg.Point(11.4, 4.5, 500)
        self.assertEqual(self.tsg1, mg.TS_Geometry(sg.Point(11.4, 4.5, 500), dt.datetime(2017, 07, 25, 20, 0, 0)))
        
    def test_has_z(self):
        
        self.assertEqual(self.tsg1.has_z, True)
        self.assertEqual(self.tsg2.has_z, False)
        
    def test_crs(self):
        
        tsg_x = mg.TS_Geometry(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326"))
        self.assertEqual(tsg_x.crs.srs, pyproj.Proj(init="epsg:4326").srs)
        self.assertEqual(self.tsg1.crs, None)
        
    def test_eq(self):
        
        tsg_x1 = mg.TS_Geometry(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326"))
        tsg_x2 = mg.TS_Geometry(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:32631"))
        tsg_x3 = mg.TS_Geometry(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0))
        
        self.assertFalse(tsg_x1 == tsg_x2)
        self.assertFalse(tsg_x2 == tsg_x3)
        self.assertTrue(tsg_x1 == mg.TS_Geometry(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326")))
        self.assertTrue(tsg_x3 == mg.TS_Geometry(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0)))
        
    def test_reproject(self):
         
        tsg_x1 = mg.TS_Geometry(sg.Point(10.5, 48, 500), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326"))
         
        # test if ValueError is raised if TS_Geometry.crs is None
        with self.assertRaises(ValueError):
            self.tsg1.reproject(pyproj.Proj(init="epsg:32631"))
             
        # test if TypeErrror is raised if type to_crs is not pyproj.Proj
        with self.assertRaises(TypeError):
            tsg_x1.reproject(32631)
         
        tsg_x1.reproject(pyproj.Proj(init="epsg:32631"))
        self.assertEqual(tsg_x1.crs.srs, pyproj.Proj(init="epsg:32631").srs)
        self.assertEqual(tsg_x1.value, sg.Point(1059297.06378364, 5343577.901783184, 500))


class Test_TS_Point(unittest.TestCase):
    
    def setUp(self):
        self.tsp1 = mg.TS_Point(sg.Point(10.2, 2.4, 460), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tsp2 = mg.TS_Point(sg.Point(12.2, 10.4), zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 10)))
        
    def test_init(self):
        
        # test if TypeError is raised if value not of type shapely.geometry.Point
        with self.assertRaises(TypeError):
            mg.TS_Point(123, dt.datetime(2017, 07, 25, 20, 0, 0))
            
        # test if ValueError is raised if shapely.geometry.Point is empty
        with self.assertRaises(ValueError):
            mg.TS_Point(sg.Point(), dt.datetime(2017, 07, 25, 20, 0, 0))
                
        # test if TypeError is raised when ts is not of type datetime.datetime and ts is not of type Time_Period
        with self.assertRaises(TypeError):
            mg.TS_Point(sg.Point(10.2, 2.4, 460), 123)
            
        # test if TypeError is raised if crs is not of type pyproj.Proj
        with self.assertRaises(TypeError):
            mg.TS_Point(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0), 123)
            
    def test_value(self):
        
        # test if correct value is returned
        self.assertEqual(self.tsp1.value, sg.Point(10.2, 2.4, 460))
        
        # test if TypeError is raised if assigned value is not of type shapely.geometry.Point
        with self.assertRaises(TypeError):
            self.tsp1.value = 123
            
        # test if ValueError is raised if self.has_z != value.has_z
        with self.assertRaises(ValueError):
            self.tsp1.value = sg.Point(11.4, 4.5)
            
        with self.assertRaises(ValueError):
            self.tsp2.value = sg.Point(11.4, 4.5, 500)
            
        # test if correct value is assigned
        self.tsp1.value = sg.Point(11.4, 4.5, 500)
        self.assertEqual(self.tsp1, mg.TS_Point(sg.Point(11.4, 4.5, 500), dt.datetime(2017, 07, 25, 20, 0, 0)))
        
    def test_has_z(self):
        
        self.assertEqual(self.tsp1.has_z, True)
        self.assertEqual(self.tsp2.has_z, False)
        
    def test_crs(self):
        
        tsp_x = mg.TS_Point(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326"))
        self.assertEqual(tsp_x.crs.srs, pyproj.Proj(init="epsg:4326").srs)
        
    def test_eq(self):
        
        tsp_x1 = mg.TS_Point(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326"))
        tsp_x2 = mg.TS_Point(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:32631"))
        tsp_x3 = mg.TS_Point(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0))
        
        self.assertFalse(tsp_x1 == tsp_x2)
        self.assertFalse(tsp_x2 == tsp_x3)
        self.assertTrue(tsp_x1 == mg.TS_Point(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326")))
        self.assertTrue(tsp_x3 == mg.TS_Point(sg.Point(10.2, 21), dt.datetime(2017, 07, 25, 20, 0, 0)))
        
    def test_reproject(self):
         
        tsp_x1 = mg.TS_Point(sg.Point(10.5, 48, 500), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326"))
         
        # test if ValueError is raised if TS_Point.crs is None
        with self.assertRaises(ValueError):
            self.tsp1.reproject(pyproj.Proj(init="epsg:32631"))
             
        # test if TypeErrror is raised if type to_crs is not pyproj.Proj
        with self.assertRaises(TypeError):
            tsp_x1.reproject(32631)
         
        tsp_x1.reproject(pyproj.Proj(init="epsg:32631"))
        self.assertEqual(tsp_x1.crs.srs, pyproj.Proj(init="epsg:32631").srs)
        self.assertEqual(tsp_x1.value, sg.Point(1059297.06378364, 5343577.901783184, 500))
        

class Test_Moving_Point(unittest.TestCase):
    
    def setUp(self):
        
        self.tsu1 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.tsu2 = zeit.TS_Unit(IPoint.linear_point, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.tsu3 = zeit.TS_Unit(IPoint.curve_point, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        
        self.tsp1 = mg.TS_Point(sg.Point(1, 1), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tsp2 = mg.TS_Point(sg.Point(1, 2), dt.datetime(2017, 07, 25, 20, 0, 5))
        self.tsp3 = mg.TS_Point(sg.Point(2, 2), dt.datetime(2017, 07, 25, 20, 0, 10))
        self.tsp4 = mg.TS_Point(sg.Point(3, 2), dt.datetime(2017, 07, 25, 20, 0, 20))
        self.tsp5 = mg.TS_Point(sg.Point(4, 1), dt.datetime(2017, 07, 25, 20, 0, 30))
        
        self.c1 = sg.LineString([(3,2),(4,2),(4,1)])
        
    def test_init(self):
        
        # test if ValueError is raised if ts_object_list is empty
        with self.assertRaises(ValueError):
            mg.Moving_Point([], self.ip)
        
        # test if TypeError is raised if not all elements in ts_object list are of type sptemp.moving_geometry.TS_Point
        with self.assertRaises(TypeError):
            mg.Moving_Point([self.tsp1, 123], self.ip)
            
        with self.assertRaises(TypeError):
            mg.Moving_Point([self.tsp1, zeit.TS_Object(sg.Point(1, 1), dt.datetime(2017, 07, 25, 20, 0, 5))], self.ip)
            
        # test if ValueErrror is raised if crs of TS_Points is not equal
        with self.assertRaises(ValueError):
            mg.Moving_Point([self.tsp1, mg.TS_Point(sg.Point(1, 2), dt.datetime(2017, 07, 25, 20, 0, 5), pyproj.Proj(init="epsg:32631"))], self.ip)
            
        with self.assertRaises(ValueError):
            mg.Moving_Point([mg.TS_Point(sg.Point(1, 1), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326")),
                             mg.TS_Point(sg.Point(1, 2), dt.datetime(2017, 07, 25, 20, 0, 5), pyproj.Proj(init="epsg:32631"))], self.ip)
            
        # test if ValueError is raised if has_z of Ts_Points is not equal
        with self.assertRaises(ValueError):
            mg.Moving_Point([self.tsp1, mg.TS_Point(sg.Point(1, 2, 5), dt.datetime(2017, 07, 25, 20, 0, 5))], self.ip)
            
    def test_has_z(self):
        
        self.assertEqual(self.tsp1.has_z, False)
        self.assertEqual(mg.TS_Point(sg.Point(1, 2, 5), dt.datetime(2017, 07, 25, 20, 0, 5)).has_z, True)
        
    def test_crs(self):
        
        self.assertEqual(self.tsp1.crs, None)
        self.assertEqual(mg.TS_Point(sg.Point(1, 2, 5), dt.datetime(2017, 07, 25, 20, 0, 5), pyproj.Proj(init="epsg:4326")).crs.srs,
                         pyproj.Proj(init="epsg:4326").srs)
        
    def test_setitem(self):
        
        mp1 = mg.Moving_Point([self.tsp1, self.tsp2, self.tsp3, self.tsp4, self.tsp5], self.ip)
        mp2 = mg.Moving_Point([mg.TS_Point(sg.Point(1, 1), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:32631")),
                               mg.TS_Point(sg.Point(4, 1), dt.datetime(2017, 07, 25, 20, 0, 30), pyproj.Proj(init="epsg:32631"))],self.ip)
        
        # test if TypeError is raised if key not of type int
        with self.assertRaises(TypeError):
            mp1[0:2] = mg.TS_Point(sg.Point(1, 2), dt.datetime(2017, 07, 25, 20, 0, 0))
            
        # test if TypeError is raised if value not of type sptemp.moving_geometry.TS_Point
        with self.assertRaises(TypeError):
            mp1[0] = zeit.TS_Object(sg.Point(1, 2), dt.datetime(2017, 07, 25, 20, 0, 0))
            
        # test if ValueError is raised if value.has_z != self.has_z
        with self.assertRaises(ValueError):
            mp1[0] = mg.TS_Point(sg.Point(1, 2, 5), dt.datetime(2017, 07, 25, 20, 0, 0))
        
        # test if ValueError is raised if value.crs != self.crs
        with self.assertRaises(ValueError):
            mp2[0] = mg.TS_Point(sg.Point(1, 2), dt.datetime(2017, 07, 25, 20, 0, 0))
            
        with self.assertRaises(ValueError):
            mp2[0] = mg.TS_Point(sg.Point(1, 2), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326"))
            
        # test if ValueError is raised if value.ts and other TS_Points in Moving_Object are not disjoint
        with self.assertRaises(ValueError):
            mp1[0] = mg.TS_Point(sg.Point(2, 2), dt.datetime(2017, 07, 25, 20, 0, 5))
            
        # test if value is set correctly
        mp1[0] = mg.TS_Point(sg.Point(2, 2), zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 1), dt.datetime(2017, 07, 25, 20, 0, 4)))
        self.assertEqual(mp1[0], mg.TS_Point(sg.Point(2, 2), zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 1), dt.datetime(2017, 07, 25, 20, 0, 4))))
        
    def test_interpolate(self):
        
        mp1 = mg.Moving_Point([self.tsp1, self.tsp2, self.tsp3, self.tsp4, self.tsp5], self.ip)
        
        # test if TypeError is raised if time not of tyoe dt.datetime
        with self.assertRaises(TypeError):
            mp1.interpolate(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 1), dt.datetime(2017, 07, 25, 20, 0, 4)))
            
        # test if None is returned if time < Moving_Object.start_time() or > Moving_Object.end_time()
        self.assertEqual(mp1.interpolate(dt.datetime(2017, 07, 25, 19, 0, 1)), None)
        self.assertEqual(mp1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 31)), None)
        
        # test if correctly interpolated values are returned
        self.assertEqual(mp1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 1)).value, sg.Point(1,1))
        self.assertEqual(mp1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 7)).value, sg.Point(1,2))
        self.assertEqual(mp1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 11)).value, sg.Point(2.1,2))
        self.assertEqual(mp1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 20)).value, sg.Point(3,2))
        self.assertEqual(mp1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 25), self.c1).value, sg.Point(4,2))
        self.assertEqual(mp1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 30), self.c1).value, sg.Point(4,1))
        
    def test_slice(self):
        
        # test if sptemp.moving_geometry.Moving_Point is returned
        mp1 = mg.Moving_Point([self.tsp1, self.tsp2, self.tsp3, self.tsp4, self.tsp5], self.ip)
        mp_slice = mp1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 1), dt.datetime(2017, 07, 25, 20, 0, 18)))
        self.assertEqual(len(mp_slice), 2)
        self.assertTrue(isinstance(mp_slice, mg.Moving_Point))
        
    def test_resampled_slice(self):
        
        # test if sptemp.moving_geometry.Moving_Point is returned
        mp1 = mg.Moving_Point([self.tsp1, self.tsp2, self.tsp3, self.tsp4, self.tsp5], self.ip)
        mp_reslice = mp1.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 7), dt.datetime(2017, 07, 25, 20, 0, 15)])
        self.assertEqual(len(mp_reslice), 3)
        self.assertTrue(isinstance(mp_reslice, mg.Moving_Point))
        
    def test_append(self):
        
        mp1 = mg.Moving_Point([self.tsp1, self.tsp2, self.tsp3, self.tsp4, self.tsp5], self.ip)
        
        # test if TypeError is raised if value is not of type TS_Point
        with self.assertRaises(TypeError):
            mp1.append(zeit.TS_Object(sg.Point(4, 2), dt.datetime(2017, 07, 25, 20, 0, 40)))
            
        # test if ValueError is raised if value.start_time() <= Moving_Point.end_time()
        with self.assertRaises(ValueError):
            mp1.append(mg.TS_Point(sg.Point(4, 2), dt.datetime(2017, 07, 25, 20, 0, 25)))
            
        # test if ValueError is raised if coordinate dimension is inconsistent
        with self.assertRaises(ValueError):
            mp1.append(mg.TS_Point(sg.Point(4, 2, 1), dt.datetime(2017, 07, 25, 20, 0, 35)))
            
        # test if ValueError is raised if crs is inconsistent
        with self.assertRaises(ValueError):
            mp1.append(mg.TS_Point(sg.Point(4, 2), dt.datetime(2017, 07, 25, 20, 0, 35), pyproj.Proj(init="epsg:4326")))
            
        # test if value is appended correctly
        mp1.append(mg.TS_Point(sg.Point(4, 2), dt.datetime(2017, 07, 25, 20, 0, 35)))
        
        self.assertEqual(len(mp1), 6)
        self.assertEqual(mp1[-1], mg.TS_Point(sg.Point(4, 2), dt.datetime(2017, 07, 25, 20, 0, 35)))
    
    def test_insert(self):
        
        mp1 = mg.Moving_Point([self.tsp1, self.tsp2, self.tsp3, self.tsp4, self.tsp5], self.ip)
        
        # test if TypeError is raised if value is not of type TS_Point
        with self.assertRaises(TypeError):
            mp1.insert(zeit.TS_Object(sg.Point(4, 2), dt.datetime(2017, 07, 25, 20, 0, 25)))
            
        # test if ValueError is raised if coordinate dimension is inconsistent
        with self.assertRaises(ValueError):
            mp1.insert(mg.TS_Point(sg.Point(4, 2, 1), dt.datetime(2017, 07, 25, 20, 0, 25)))
            
        # test if ValueError is raised if crs is inconsistent
        with self.assertRaises(ValueError):
            mp1.insert(mg.TS_Point(sg.Point(4, 2), dt.datetime(2017, 07, 25, 20, 0, 25), pyproj.Proj(init="epsg:4326")))
            
        # test if value is inserted correctly
        mp1.insert(mg.TS_Point(sg.Point(4, 2), dt.datetime(2017, 07, 25, 20, 0, 25)))
        
        self.assertEqual(len(mp1), 6)
        self.assertEqual(mp1[4], mg.TS_Point(sg.Point(4, 2), dt.datetime(2017, 07, 25, 20, 0, 25)))
    
    def test_within(self):
        
        time_d1 = dt.timedelta(seconds=1)
        time_d2 = dt.timedelta(milliseconds=10)
        
        poly = sg.Polygon([(2,2),(5,2),(5,5),(2,5),(2,2)])
        line = sg.LineString([(3,1),(3,3.5),(1,3.5)])
        
        # test with polygon
        ip1 = zeit.Interpolator([zeit.TS_Unit(IPoint.curve_point, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10)))])
        ip2 = zeit.Interpolator([zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10)))])
        ip3 = zeit.Interpolator([zeit.TS_Unit(IRing.linear_translation, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10)))])
        tsp1 = mg.TS_Point(sg.Point(3,1), dt.datetime(2017, 07, 25, 20, 0, 0))
        tsp2 = mg.TS_Point(sg.Point(1,3.5), dt.datetime(2017, 07, 25, 20, 0, 9))
        mp1 = mg.Moving_Point([tsp1,tsp2],ip1)
        arg_mo1 = zeit.Moving_Object([zeit.TS_Object([line], zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10)))],ip2)
        
        # test with polygon
        self.assertEqual([x.ts for x in mp1.within(poly, time_d1, time_d2, arg_mo1)],
                         [dt.datetime(2017, 7, 25, 20, 0), dt.datetime(2017, 7, 25, 20, 0, 2, 10000),
                          dt.datetime(2017, 7, 25, 20, 0, 7), dt.datetime(2017, 7, 25, 20, 0, 9)])
        self.assertEqual([x.value for x in mp1.within(poly, time_d1, time_d2, arg_mo1)], [False, True, False, False])
        
        # test with TS_Geometry
        tspol1 = mg.TS_Geometry(poly, zeit.Time_Period(dt.datetime(2017, 7, 25, 20, 0, 5), dt.datetime(2017, 7, 25, 20, 0, 8)))
        
        self.assertEqual([x.ts for x in mp1.within(tspol1, time_d1, time_d2, arg_mo1)],
                         [dt.datetime(2017, 7, 25, 20, 0), dt.datetime(2017, 7, 25, 20, 0, 5),
                          dt.datetime(2017, 7, 25, 20, 0, 7), dt.datetime(2017, 7, 25, 20, 0, 9)])
        self.assertEqual([x.value for x in mp1.within(tspol1, time_d1, time_d2, arg_mo1)], [False, True, False, False])
        
        # test with Moving_Collection
        tslr1 = mg.TS_LinearRing(sg.LinearRing([(2,2),(5,2),(5,5),(2,5),(2,2)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        tslr2 = mg.TS_LinearRing(sg.LinearRing([(2,3),(5,3),(5,6),(2,6),(2,3)]), dt.datetime(2017, 07, 25, 20, 0, 9))
        mlr = mg.Moving_LinearRing([tslr1,tslr2],ip3)
        mpol = mg.Moving_Polygon(mlr)

        self.assertEqual([x.ts for x in mp1.within(mpol, time_d1, time_d2, arg_mo1)],
                         [dt.datetime(2017, 7, 25, 20, 0), dt.datetime(2017, 7, 25, 20, 0, 2, 580000),
                          dt.datetime(2017, 7, 25, 20, 0, 7), dt.datetime(2017, 7, 25, 20, 0, 9)])
        self.assertEqual([x.value for x in mp1.within(mpol, time_d1, time_d2, arg_mo1)], [False, True, False, False])
        
    def test_reproject(self):
        
        mp1 = mg.Moving_Point([self.tsp1, self.tsp2, self.tsp3, self.tsp4, self.tsp5], self.ip)
        mp2 = mg.Moving_Point([mg.TS_Point(sg.Point(10.2, 48.1), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326")),
                               mg.TS_Point(sg.Point(10.7, 48.5), dt.datetime(2017, 07, 25, 20, 0, 30), pyproj.Proj(init="epsg:4326"))], self.ip)
         
        # test if ValueError is raised if Moving_Object.crs is None
        with self.assertRaises(ValueError):
            mp1.reproject(pyproj.Proj(init="epsg:32631"))
             
        # test if TypeError is raised if to_crs not of type pyproj.Proj
        with self.assertRaises(TypeError):
            mp2.reproject(123)
             
        # test if coordinates are repojected correctly
        mp2.reproject(pyproj.Proj(init="epsg:32631"))
        self.assertEqual(mp2.crs.srs, pyproj.Proj(init="epsg:32631").srs)
        self.assertEqual(mp2[0].value, sg.Point(1035894.8206676971,5352539.675035289))
    
        
class Test_TS_LineString(unittest.TestCase):
    
    def setUp(self):
        self.tsl1 = mg.TS_LineString(sg.LineString([(10, 48, 500), (11, 48.5, 490)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tsl2 = mg.TS_LineString(sg.LineString([(10, 48), (11, 48.5)]), zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 10)))
        
    def test_init(self):
        
        # test if TypeError is raised if value not of type shapely.geometry.LineString
        with self.assertRaises(TypeError):
            mg.TS_LineString(sg.Point(10,20), dt.datetime(2017, 07, 25, 20, 0, 0))
            
        # test if ValueError is raised if shapely.geometry.LineString is empty
        with self.assertRaises(ValueError):
            mg.TS_LineString(sg.LineString(), dt.datetime(2017, 07, 25, 20, 0, 0))
                
        # test if TypeError is raised when ts is not of type datetime.datetime and ts is not of type Time_Period
        with self.assertRaises(TypeError):
            mg.TS_LineString(sg.LineString([(10, 48), (11, 48.5)]), 123)
            
        # test if TypeError is raised if crs is not of type pyproj.Proj
        with self.assertRaises(TypeError):
            mg.TS_LineString(sg.LineString([(10, 48), (11, 48.5)]), dt.datetime(2017, 07, 25, 20, 0, 0), 123)
            
    def test_value(self):
        
        # test if correct value is returned
        self.assertEqual(self.tsl2.value, sg.LineString([(10, 48), (11, 48.5)]))
        
        # test if TypeError is raised if assigned value is not of type shapely.geometry.Point
        with self.assertRaises(TypeError):
            self.tsl1.value = sg.Point(11.4, 4.5)
            
        # test if ValueError is raised if self.has_z != value.has_z
        with self.assertRaises(ValueError):
            self.tsl1.value = sg.LineString([(10, 48), (11, 48.5)])
            
        with self.assertRaises(ValueError):
            self.tsl2.value = sg.LineString([(10, 48, 500), (11, 48.5, 490)])
            
        # test if correct value is assigned
        self.tsl2.value = sg.LineString([(10.5, 48.2), (11, 48.5)])
        self.assertEqual(self.tsl2.value, sg.LineString([(10.5, 48.2), (11, 48.5)]))
        
    def test_has_z(self):
        
        self.assertEqual(self.tsl1.has_z, True)
        self.assertEqual(self.tsl2.has_z, False)
        
    def test_crs(self):
        
        tsl_x = mg.TS_LineString(sg.LineString([(10, 48), (11, 48.5)]), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326"))
        self.assertEqual(tsl_x.crs.srs, pyproj.Proj(init="epsg:4326").srs)
        
    def test_eq(self):
        
        tsl_x1 = mg.TS_LineString(sg.LineString([(10, 48), (11, 48.5)]), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326"))
        tsl_x2 = mg.TS_LineString(sg.LineString([(10, 48), (11, 48.5)]), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:32631"))
        tsl_x3 = mg.TS_LineString(sg.LineString([(10, 48), (11, 48.5)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        tsl_x4 = mg.TS_LineString(sg.LineString([(10, 48, 500), (11, 48.5, 500)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        
        self.assertFalse(tsl_x1 == tsl_x2)
        self.assertFalse(tsl_x2 == tsl_x3)
        self.assertFalse(tsl_x3 == tsl_x4)
        self.assertTrue(tsl_x1 == mg.TS_LineString(sg.LineString([(10, 48), (11, 48.5)]), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326")))
        self.assertTrue(tsl_x3 == mg.TS_LineString(sg.LineString([(10, 48), (11, 48.5)]), dt.datetime(2017, 07, 25, 20, 0, 0)))
        
        
class Test_Moving_LineString(unittest.TestCase):
    
    def setUp(self):
        
        self.tsu1 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.tsu2 = zeit.TS_Unit(ICurve.basic_linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.ip = zeit.Interpolator([self.tsu1, self.tsu2])
        
        self.tsl1 = mg.TS_LineString(sg.LineString([(2,0),(1,1),(1.5,2),(2.5,2.5),(2.5,3.5)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tsl2 = mg.TS_LineString(sg.LineString([(5.5,0),(5,1),(6,2.5)]), dt.datetime(2017, 07, 25, 20, 0, 10))
        self.tsl3 = mg.TS_LineString(sg.LineString([(7,0),(7,1),(8,1.5),(9,3)]), dt.datetime(2017, 07, 25, 20, 0, 20))
        
        self.t1 = dt.datetime(2017, 07, 25, 20, 0, 5)
        self.t2 = dt.datetime(2017, 07, 25, 20, 0, 15)
        
    def test_init(self):
        
        # test if ValueError is raised if ts_object_list is empty
        with self.assertRaises(ValueError):
            mg.Moving_LineString([], self.ip)
        
        # test if TypeError is raised if not all elements in ts_object list are of type sptemp.moving_geometry.Ts_LineString
        with self.assertRaises(TypeError):
            mg.Moving_LineString([self.tsl1, 123], self.ip)
            
        with self.assertRaises(TypeError):
            mg.Moving_LineString([self.tsl1, zeit.TS_Object(sg.LineString([(7,0),(7,1),(8,1.5),(9,3)]), dt.datetime(2017, 07, 25, 20, 0, 5))], self.ip)
            
        # test if ValueErrror is raised if crs of Ts_LineStrings is not equal
        with self.assertRaises(ValueError):
            mg.Moving_LineString([self.tsl1, mg.TS_LineString(sg.LineString([(7,0),(7,1),(8,1.5),(9,3)]),
                                                    dt.datetime(2017, 07, 25, 20, 0, 5), pyproj.Proj(init="epsg:32631"))], self.ip)
            
        with self.assertRaises(ValueError):
            mg.Moving_LineString([mg.TS_LineString(sg.LineString([(2,0),(1,1),(1.5,2),(2.5,2.5),(2.5,3.5)]),
                                                   dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326")),
                                  mg.TS_LineString(sg.LineString([(7,0),(7,1),(8,1.5),(9,3)]),
                                                   dt.datetime(2017, 07, 25, 20, 0, 5), pyproj.Proj(init="epsg:32631"))], self.ip)
            
        # test if ValueError is raised if has_z of Ts_LineStrings is not equal
        with self.assertRaises(ValueError):
            mg.Moving_LineString([self.tsl1, mg.TS_LineString(sg.LineString([(7,0,1),(7,1,2),(8,1.5,3),(9,3,2)]), dt.datetime(2017, 07, 25, 20, 0, 5))], self.ip)
            
    def test_has_z(self):
        
        self.assertEqual(self.tsl1.has_z, False)
        self.assertEqual(mg.TS_LineString(sg.LineString([(7,0,1),(7,1,2),(8,1.5,3),(9,3,2)]), dt.datetime(2017, 07, 25, 20, 0, 5)).has_z, True)
        
    def test_crs(self):
        
        self.assertEqual(self.tsl1.crs, None)
        self.assertEqual(mg.TS_LineString(sg.LineString([(2,0),(1,1),(1.5,2),(2.5,2.5),(2.5,3.5)]),
                                          dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326")).crs.srs,
                                          pyproj.Proj(init="epsg:4326").srs)
        
    def test_setitem(self):
        
        ml1 = mg.Moving_LineString([self.tsl1, self.tsl2, self.tsl3], self.ip)
        ml2 = mg.Moving_LineString([mg.TS_LineString(sg.LineString([(2,0),(1,1),(1.5,2),(2.5,2.5),(2.5,3.5)]),
                                                     dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:32631")),
                               mg.TS_LineString(sg.LineString([(5.5,0),(5,1),(6,2.5)]),
                                                dt.datetime(2017, 07, 25, 20, 0, 10), pyproj.Proj(init="epsg:32631"))],self.ip)
        
        # test if TypeError is raised if key not of type int
        with self.assertRaises(TypeError):
            ml1[0:2] = mg.TS_LineString(sg.LineString([(6,0),(5,1),(6,2.5)]), dt.datetime(2017, 07, 25, 20, 0, 15))
            
        # test if TypeError is raised if value not of type sptemp.moving_geometry.TS_LineString
        with self.assertRaises(TypeError):
            ml1[1] = zeit.TS_Object(sg.LineString([(6,0),(5,1),(6,2.5)]), dt.datetime(2017, 07, 25, 20, 0, 15))
            
        # test if ValueError is raised if value.has_z != self.has_z
        with self.assertRaises(ValueError):
            ml1[1] = mg.TS_LineString(sg.LineString([(6,0,5),(5,1,4),(6,2.5,8)]), dt.datetime(2017, 07, 25, 20, 0, 15))
        
        # test if ValueError is raised if value.crs != self.crs
        with self.assertRaises(ValueError):
            ml2[1] = mg.TS_LineString(sg.LineString([(6,0),(5,1),(6,2.5)]), dt.datetime(2017, 07, 25, 20, 0, 15))
            
        with self.assertRaises(ValueError):
            ml2[1] = mg.TS_LineString(sg.LineString([(6,0),(5,1),(6,2.5)]), dt.datetime(2017, 07, 25, 20, 0, 15), pyproj.Proj(init="epsg:4326"))
            
        # test if ValueError is raised if value.ts and other TS_Points in Moving_Object are not disjoint
        with self.assertRaises(ValueError):
            ml1[1] = mg.TS_LineString(sg.LineString([(6,0),(5,1),(6,2.5)]), dt.datetime(2017, 07, 25, 19, 0, 20))
            
        # test if value is set correctly
        ml1[1] = mg.TS_LineString(sg.LineString([(6,0),(5,1),(6,2.5)]), dt.datetime(2017, 07, 25, 20, 0, 15))
        self.assertEqual(ml1[1], mg.TS_LineString(sg.LineString([(6,0),(5,1),(6,2.5)]), dt.datetime(2017, 07, 25, 20, 0, 15)))
        
    def test_interpolate(self):
        
        ml1 = mg.Moving_LineString([self.tsl1, self.tsl2, self.tsl3], self.ip)
        
        # test if TypeError is raised if time not of type datetime.datetime
        with self.assertRaises(TypeError):
            ml1.interpolate(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 1), dt.datetime(2017, 07, 25, 20, 0, 4)))
            
        # test if None is returned if time < Moving_Object.start_time() or > Moving_Object.end_time()
        self.assertEqual(ml1.interpolate(dt.datetime(2017, 07, 25, 19, 0, 1)), None)
        self.assertEqual(ml1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 31)), None)
        
        # test if correctly interpolated values are returne
        self.assertEqual(ml1.interpolate(self.t1).value, sg.LineString([(2,0),(1,1),(1.5,2),(2.5,2.5),(2.5,3.5)]))
        self.assertEqual(ml1.interpolate(self.t2).value, sg.LineString([(6.25, 0.0), (6.0, 1.0), (6.691391109268659, 1.537086663902989), (7.5, 2.75)]))
        
    def test_slice(self):
        
        # test if sptemp.moving_geometry.Moving_LineString is returned
        ml1 = mg.Moving_LineString([self.tsl1, self.tsl2, self.tsl3], self.ip)
        ml_slice = ml1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 1), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.assertEqual(len(ml_slice), 2)
        self.assertTrue(isinstance(ml_slice, mg.Moving_LineString))
        
    def test_resampled_slice(self):
        
        # test if sptemp.moving_geometry.Moving_LineString is returned
        ml1 = mg.Moving_LineString([self.tsl1, self.tsl2, self.tsl3], self.ip)
        ml_reslice = ml1.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 7), dt.datetime(2017, 07, 25, 20, 0, 15)])
        self.assertEqual(len(ml_reslice), 3)
        self.assertTrue(isinstance(ml_reslice, mg.Moving_LineString))
        
    def test_append(self):
        
        ml1 = mg.Moving_LineString([self.tsl1, self.tsl2, self.tsl3], self.ip)
        
        # test if TypeError is raised if value is not of type TS_LineString
        with self.assertRaises(TypeError):
            ml1.append(zeit.TS_Object(sg.LineString([(8,0),(7,1),(8,1.5),(9,3)]), dt.datetime(2017, 07, 25, 20, 0, 30)))
            
        # test if ValueError is raised if value.start_time() <= Moving_LineString.end_time()
        with self.assertRaises(ValueError):
            ml1.append(mg.TS_LineString(sg.LineString([(8,0),(7,1),(8,1.5),(9,3)]), dt.datetime(2017, 07, 25, 19, 0, 30)))
            
        # test if ValueError is raised if coordinate dimension is inconsistent
        with self.assertRaises(ValueError):
            ml1.append(mg.TS_LineString(sg.LineString([(8,0,1),(7,1,1),(8,1.5,1),(9,3,1)]), dt.datetime(2017, 07, 25, 20, 0, 30)))
            
        # test if ValueError is raised if crs is inconsistent
        with self.assertRaises(ValueError):
            ml1.append(mg.TS_LineString(sg.LineString([(8,0),(7,1),(8,1.5),(9,3)]), dt.datetime(2017, 07, 25, 20, 0, 30), pyproj.Proj(init="epsg:4326")))
            
        # test if value is appended correctly
        ml1.append(mg.TS_LineString(sg.LineString([(8,0),(7,1),(8,1.5),(9,3)]), dt.datetime(2017, 07, 25, 20, 0, 30)))
        
        self.assertEqual(len(ml1), 4)
        self.assertEqual(ml1[-1], mg.TS_LineString(sg.LineString([(8,0),(7,1),(8,1.5),(9,3)]), dt.datetime(2017, 07, 25, 20, 0, 30)))
    
    def test_insert(self):
        
        ml1 = mg.Moving_LineString([self.tsl1, self.tsl2, self.tsl3], self.ip)
        
        # test if TypeError is raised if value is not of type TS_LineString
        with self.assertRaises(TypeError):
            ml1.insert(zeit.TS_Object(sg.LineString([(0,0),(1,1),(1.5,2),(2.5,2.5),(2.5,3.5)]), dt.datetime(2017, 07, 25, 19, 0, 25)))
            
        # test if ValueError is raised if coordinate dimension is inconsistent
        with self.assertRaises(ValueError):
            ml1.insert(mg.TS_LineString(sg.LineString([(0,0,1),(1,1,1),(1.5,2,1),(2.5,2.5,1),(2.5,3.5,1)]), dt.datetime(2017, 07, 25, 19, 0, 25)))
            
        # test if ValueError is raised if crs is inconsistent
        with self.assertRaises(ValueError):
            ml1.insert(mg.TS_LineString(sg.LineString([(0,0),(1,1),(1.5,2),(2.5,2.5),(2.5,3.5)]), dt.datetime(2017, 07, 25, 19, 0, 25), pyproj.Proj(init="epsg:4326")))
            
        # test if value is inserted correctly
        ml1.insert(mg.TS_LineString(sg.LineString([(0,0),(1,1),(1.5,2),(2.5,2.5),(2.5,3.5)]), dt.datetime(2017, 07, 25, 19, 0, 25)))
        
        self.assertEqual(len(ml1), 4)
        self.assertEqual(ml1[0], mg.TS_LineString(sg.LineString([(0,0),(1,1),(1.5,2),(2.5,2.5),(2.5,3.5)]), dt.datetime(2017, 07, 25, 19, 0, 25)))
    
    
class Test_TS_LinearRing(unittest.TestCase):
    
    def setUp(self):
        self.tslr1 = mg.TS_LinearRing(sg.LinearRing([(1, 1, 2), (2, 1, 2), (2, 2, 2), (1, 2, 1), (1, 1, 2)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tslr2 = mg.TS_LinearRing(sg.LinearRing([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)]), dt.datetime(2017, 07, 25, 20, 0, 10))
        
    def test_init(self):
        
        # test if TypeError is raised if value not of type shapely.geometry.LinearRing
        with self.assertRaises(TypeError):
            mg.TS_LinearRing(sg.LineString([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)]), dt.datetime(2017, 07, 25, 20, 0, 10))
            
        # test if ValueError is raised if shapely.geometry.LinearRing is empty
        with self.assertRaises(ValueError):
            mg.TS_LinearRing(sg.LinearRing(), dt.datetime(2017, 07, 25, 20, 0, 0))
                
        # test if TypeError is raised when ts is not of type datetime.datetime and ts is not of type Time_Period
        with self.assertRaises(TypeError):
            mg.TS_LinearRing(sg.LinearRing([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)]), 123)
            
        # test if TypeError is raised if crs is not of type pyproj.Proj
        with self.assertRaises(TypeError):
            mg.TS_LinearRing(sg.LinearRing([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)]), dt.datetime(2017, 07, 25, 20, 0, 10), 123)
            
    def test_value(self):
        
        # test if correct value is returned
        self.assertEqual(self.tslr2.value, sg.LinearRing([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)]))
        
        # test if TypeError is raised if assigned value is not of type shapely.geometry.LinearRing
        with self.assertRaises(TypeError):
            self.tslr2.value = sg.LineString([(1.1, 1), (2, 1), (2, 2), (1, 2), (1, 1)])
            
        # test if ValueError is raised if self.has_z != value.has_z
        with self.assertRaises(ValueError):
            self.tslr1.value = sg.LinearRing([(1.1, 1), (2, 1), (2, 2), (1, 2), (1, 1)])
            
        # test if correct value is assigned
        self.tslr2.value = sg.LinearRing([(1.1, 1), (2, 1), (2, 2), (1, 2), (1, 1)])
        self.assertEqual(self.tslr2.value, sg.LinearRing([(1.1, 1), (2, 1), (2, 2), (1, 2), (1, 1)]))
        

class Test_Moving_LinearRing(unittest.TestCase):
    
    def setUp(self):
        
        self.tsu1 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 2)))
        self.tsu2 = zeit.TS_Unit(IRing.linear_translation, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 2), dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.ip = zeit.Interpolator([self.tsu1, self.tsu2])
        
        self.tslr1 = mg.TS_LinearRing(sg.LinearRing([(1,1),(2,1),(2,2),(1,2),(1,1)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tslr2 = mg.TS_LinearRing(sg.LinearRing([(3,1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 10))
        
        self.t1 = dt.datetime(2017, 07, 25, 20, 0, 2)
        self.t2 = dt.datetime(2017, 07, 25, 20, 0, 6)
        
    def test_init(self):
        
        # test if ValueError is raised if ts_object_list is empty
        with self.assertRaises(ValueError):
            mg.Moving_LinearRing([], self.ip)
        
        # test if TypeError is raised if not all elements in ts_object list are of type sptemp.moving_geometry.Ts_LinearRing
        with self.assertRaises(TypeError):
            mg.Moving_LinearRing([self.tslr1, 123], self.ip)
            
        with self.assertRaises(TypeError):
            mg.Moving_LinearRing([self.tslr1, mg.TS_LineString(sg.LinearRing([(3,1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 10))], self.ip)
            
        # test if ValueErrror is raised if crs of Ts_LinearRings is not equal
        with self.assertRaises(ValueError):
            mg.Moving_LinearRing([self.tslr1, mg.TS_LinearRing(sg.LinearRing([(3,1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 10),
                                                               pyproj.Proj(init="epsg:32631"))], self.ip)
            
        with self.assertRaises(ValueError):
            mg.Moving_LinearRing([mg.TS_LinearRing(sg.LinearRing([(1,1),(2,1),(2,2),(1,2),(1,1)]), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326")),
                                  mg.TS_LinearRing(sg.LinearRing([(3,1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 10), pyproj.Proj(init="epsg:32631"))],
                                  self.ip)
            
        # test if ValueError is raised if has_z of Ts_LinearRings is not equal
        with self.assertRaises(ValueError):
            mg.Moving_LinearRing([mg.TS_LinearRing(sg.LinearRing([(1,1,2),(2,1,2),(2,2,1),(1,2,1),(1,1,2)]), dt.datetime(2017, 07, 25, 20, 0, 0)),
                                  mg.TS_LinearRing(sg.LinearRing([(3,1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 10))], self.ip)
        
    def test_setitem(self):
        
        mlr1 = mg.Moving_LinearRing([self.tslr1, self.tslr2], self.ip)
        
        # test if TypeError is raised if key not of type int
        with self.assertRaises(TypeError):
            mlr1[0:2] = mg.TS_LinearRing(sg.LinearRing([(1.1,1),(2,1),(2,2),(1,2),(1.1,1)]), dt.datetime(2017, 07, 25, 20, 0, 2))
            
        # test if TypeError is raised if value not of type sptemp.moving_geometry.TS_LinearRing
        with self.assertRaises(TypeError):
            mlr1[0] = mg.TS_LineString(sg.LinearRing([(1.1,1),(2,1),(2,2),(1,2),(1.1,1)]), dt.datetime(2017, 07, 25, 20, 0, 2))
            
        # test if ValueError is raised if value.has_z != self.has_z
        with self.assertRaises(ValueError):
            mlr1[0] = mg.TS_LinearRing(sg.LinearRing([(1.1,1,2),(2,1,2),(2,2,2),(1,2,2),(1.1,1,2)]), dt.datetime(2017, 07, 25, 20, 0, 2))
        
        # test if ValueError is raised if value.crs != self.crs
        with self.assertRaises(ValueError):
            mlr1[0] = mg.TS_LinearRing(sg.LinearRing([(1.1,1),(2,1),(2,2),(1,2),(1.1,1)]), dt.datetime(2017, 07, 25, 20, 0, 2), pyproj.Proj(init="epsg:4326"))
        
        # test if ValueError is raised if value.ts and other TS_Points in Moving_Object are not disjoint
        with self.assertRaises(ValueError):
            mlr1[1] = mg.TS_LinearRing(sg.LinearRing([(1.1,1),(2,1),(2,2),(1,2),(1.1,1)]), dt.datetime(2017, 07, 25, 19, 0, 2))
            
        # test if value is set correctly
        mlr1[0] = mg.TS_LinearRing(sg.LinearRing([(1.1,1),(2,1),(2,2),(1,2),(1.1,1)]), dt.datetime(2017, 07, 25, 20, 0, 2))
        self.assertEqual(mlr1[0], mg.TS_LinearRing(sg.LinearRing([(1.1,1),(2,1),(2,2),(1,2),(1.1,1)]), dt.datetime(2017, 07, 25, 20, 0, 2)))
        
    def test_interpolate(self):
        
        mlr1 = mg.Moving_LinearRing([self.tslr1, self.tslr2], self.ip)
        
        # test if TypeError is raised if time not of type datetime.datetime
        with self.assertRaises(TypeError):
            mlr1.interpolate(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 1), dt.datetime(2017, 07, 25, 20, 0, 4)))
            
        # test if None is returned if time < Moving_Object.start_time() or > Moving_Object.end_time()
        self.assertEqual(mlr1.interpolate(dt.datetime(2017, 07, 25, 19, 0, 1)), None)
        self.assertEqual(mlr1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 31)), None)
        
        # test if correctly interpolated values are return
        self.assertEqual(mlr1.interpolate(self.t1).value, sg.LinearRing([(1,1),(2,1),(2,2),(1,2),(1,1)]))
        self.assertEqual(mlr1.interpolate(self.t2).value, sg.LinearRing([(2,1),(3,1),(3,2),(2,2),(2,1)]))
        
    def test_slice(self):
        
        # test if sptemp.moving_geometry.Moving_LinearRing is returned
        mlr1 = mg.Moving_LinearRing([self.tslr1, self.tslr2], self.ip)
        mlr_slice = mlr1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 1), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.assertEqual(len(mlr_slice), 1)
        self.assertTrue(isinstance(mlr_slice, mg.Moving_LinearRing))
        
    def test_resampled_slice(self):
        
        # test if sptemp.moving_geometry.Moving_LinearRing is returned
        mlr1 = mg.Moving_LinearRing([self.tslr1, self.tslr2], self.ip)
        mlr_reslice = mlr1.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 7), dt.datetime(2017, 07, 25, 20, 0, 15)])
        self.assertEqual(len(mlr_reslice), 2)
        self.assertTrue(isinstance(mlr_reslice, mg.Moving_LinearRing))
        
    def test_append(self):
        
        mlr1 = mg.Moving_LinearRing([self.tslr1, self.tslr2], self.ip)
        
        # test if TypeError is raised if value is not of type TS_LineString
        with self.assertRaises(TypeError):
            mlr1.append(zeit.TS_Object(sg.LinearRing([(3,1.1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 20)))
            
        # test if ValueError is raised if value.start_time() <= Moving_LineString.end_time()
        with self.assertRaises(ValueError):
            mlr1.append(mg.TS_LinearRing(sg.LinearRing([(3,1.1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 0)))
            
        # test if ValueError is raised if coordinate dimension is inconsistent
        with self.assertRaises(ValueError):
            mlr1.append(mg.TS_LinearRing(sg.LinearRing([(3,1.1,1),(4,1,1),(4,2,1),(3,2,1),(3,1,1)]), dt.datetime(2017, 07, 25, 20, 0, 20)))
            
        # test if ValueError is raised if crs is inconsistent
        with self.assertRaises(ValueError):
            mlr1.append(mg.TS_LinearRing(sg.LinearRing([(3,1.1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 20), pyproj.Proj(init="epsg:4326")))
            
        # test if value is appended correctly
        mlr1.append(mg.TS_LinearRing(sg.LinearRing([(3,1.1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 20)))
        
        self.assertEqual(len(mlr1), 3)
        self.assertEqual(mlr1[-1], mg.TS_LinearRing(sg.LinearRing([(3,1.1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 20)))
        
    def test_insert(self):
        
        mlr1 = mg.Moving_LinearRing([self.tslr1, self.tslr2], self.ip)
        
        # test if TypeError is raised if value is not of type TS_LinearRing
        with self.assertRaises(TypeError):
            mlr1.insert(zeit.TS_Object(sg.LinearRing([(3,1.1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 20)))
            
        # test if ValueError is raised if coordinate dimension is inconsistent
        with self.assertRaises(ValueError):
            mlr1.insert(mg.TS_LinearRing(sg.LinearRing([(3,1.1,1),(4,1,1),(4,2,1),(3,2,1),(3,1,1)]), dt.datetime(2017, 07, 25, 20, 0, 20)))
            
        # test if ValueError is raised if crs is inconsistent
        with self.assertRaises(ValueError):
            mlr1.insert(mg.TS_LinearRing(sg.LinearRing([(3,1.1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 20), pyproj.Proj(init="epsg:4326")))
            
        # test if value is inserted correctly
        mlr1.insert(mg.TS_LinearRing(sg.LinearRing([(3,1.1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 20)))
        
        self.assertEqual(len(mlr1), 3)
        self.assertEqual(mlr1[-1], mg.TS_LinearRing(sg.LinearRing([(3,1.1),(4,1),(4,2),(3,2),(3,1)]), dt.datetime(2017, 07, 25, 20, 0, 20)))
    

class Test_Moving_Collection(unittest.TestCase):
    
    def setUp(self):
        
        self.tsu1 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.tsu2 = zeit.TS_Unit(IPoint.linear_point, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.tsu3 = zeit.TS_Unit(IPoint.curve_point, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.ip1 = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        
        self.tsp1 = mg.TS_Point(sg.Point(1, 1), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tsp2 = mg.TS_Point(sg.Point(1, 2), dt.datetime(2017, 07, 25, 20, 0, 5))
        self.tsp3 = mg.TS_Point(sg.Point(2, 2), dt.datetime(2017, 07, 25, 20, 0, 10))
        self.tsp4 = mg.TS_Point(sg.Point(3, 2), dt.datetime(2017, 07, 25, 20, 0, 20))
        self.tsp5 = mg.TS_Point(sg.Point(4, 1), dt.datetime(2017, 07, 25, 20, 0, 30))
        
        self.c1 = sg.LineString([(3,2),(4,2),(4,1)])
        
        self.mp1 = mg.Moving_Point([self.tsp1, self.tsp2, self.tsp3, self.tsp4, self.tsp5], self.ip1)
        
        self.tsu4 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.tsu5 = zeit.TS_Unit(ICurve.basic_linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.ip2 = zeit.Interpolator([self.tsu4, self.tsu5])
        
        self.tsl1 = mg.TS_LineString(sg.LineString([(2,0),(1,1),(1.5,2),(2.5,2.5),(2.5,3.5)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tsl2 = mg.TS_LineString(sg.LineString([(5.5,0),(5,1),(6,2.5)]), dt.datetime(2017, 07, 25, 20, 0, 10))
        self.tsl3 = mg.TS_LineString(sg.LineString([(7,0),(7,1),(8,1.5),(9,3)]), dt.datetime(2017, 07, 25, 20, 0, 20))
        
        self.ml1 = mg.Moving_LineString([self.tsl1, self.tsl2, self.tsl3], self.ip2)
        
        self.t1 = dt.datetime(2017, 07, 25, 20, 0, 5)
        self.t2 = dt.datetime(2017, 07, 25, 20, 0, 15)
        self.t3 = dt.datetime(2017, 07, 25, 20, 0, 25)
        
    def test_init(self):
        
        # test if ValueError is raised if moving list is empty
        with self.assertRaises(ValueError):
            mg.Moving_Collection([])
            
        # test if TypeError is raised if moving_list not of type List
        with self.assertRaises(TypeError):
            mg.Moving_Collection(self.ml1)
            
        # test if TypeError is raised if moving_list contains objects of incorrect type
        with self.assertRaises(TypeError):
            mg.Moving_Collection([self.mp1, self.ml1, self.tsl1])
            
        # test if ValueError is raised if has_z is inconsistent
        with self.assertRaises(ValueError):
            mg.Moving_Collection([self.mp1, self.ml1, mg.Moving_Point([mg.TS_Point(sg.Point(1, 1, 2), dt.datetime(2017, 07, 25, 20, 0, 0))], self.ip1)])
            
        # test if ValueError is raised if crs is inconsistent
        with self.assertRaises(ValueError):
            mg.Moving_Collection([self.mp1, self.ml1,
                                  mg.Moving_Point([mg.TS_Point(sg.Point(1, 2), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326"))], self.ip1)])
        
    def test_interpolate(self):
        
        mc1 = mg.Moving_Collection([self.mp1, self.ml1])
        a_dict = {0: [self.c1]}
        
        # test if TypeError is raised if time not of type datetime.datetime
        with self.assertRaises(TypeError):
            mc1.interpolate(123)
            
        # test if TypeErrror is raised if args_dict not of type dict
        with self.assertRaises(TypeError):
            mc1.interpolate(self.t1, [self.c1])
            
        # test if values are correctly interpolated
        mc_t1 = mc1.interpolate(self.t1, a_dict)
        self.assertTrue(isinstance(mc_t1, mg.TS_Geometry))
        self.assertEqual(mc_t1.value[1], sg.LineString([(2,0),(1,1),(1.5,2),(2.5,2.5),(2.5,3.5)]))
        
        mc_t2 = mc1.interpolate(self.t2, a_dict)
        self.assertEqual(mc_t2.value[0], sg.Point(2.5, 2))
        
        mc_t3 = mc1.interpolate(self.t3, a_dict)
        self.assertEqual(mc_t3.value[0], sg.Point(4, 2))
        
        mc_t4 = mc1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 40), a_dict)
        self.assertTrue(mc_t4 is None)
           
    def test_slice(self):
        
        mc1 = mg.Moving_Collection([self.mp1, self.ml1])
        
        s_time = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 21), dt.datetime(2017, 07, 25, 20, 0, 40))
        
        # test if TypeError is raised if time not of type sptemp.zeit.TimePeriod
        with self.assertRaises(TypeError):
            mc1.slice(123)
            
        # test if correct value is returned
        m_sl1 = mc1.slice(s_time)
        self.assertEqual(len(m_sl1.moving_list), 1)
        self.assertEqual(len(m_sl1.moving_list[0]), 1)
        
    def test_resampled_slice(self):
        
        # test if sptemp.moving_geometry.Moving_Collection is returned
        mc1 = mg.Moving_Collection([self.mp1, self.ml1])
        mc1_reslice = mc1.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 7), dt.datetime(2017, 07, 25, 20, 0, 15)])
        self.assertEqual(len(mc1_reslice.moving_list[0]), 3)
        self.assertTrue(isinstance(mc1_reslice, mg.Moving_Collection))
        
    def test_start_time(self):
        
        mc1 = mg.Moving_Collection([self.mp1, self.ml1])
        
        self.assertEqual(mc1.start_time(), dt.datetime(2017, 07, 25, 20, 0, 0))
        
    def test_end_time(self):
        
        mc1 = mg.Moving_Collection([self.mp1, self.ml1])
        
        self.assertEqual(mc1.end_time(), dt.datetime(2017, 07, 25, 20, 0, 30))
        
    def test_reproject(self):
         
        mc1 = mg.Moving_Collection([self.mp1, self.ml1])
         
        # test if ValueError is raised if self.crs is None
        with self.assertRaises(ValueError):
            mc1.reproject(pyproj.Proj(init="epsg:32631"))
             
             
        mg.Moving_Point([mg.TS_Point(sg.Point(10, 48), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326"))], self.ip1)
        mc2 = mg.Moving_Collection([mg.Moving_Point([mg.TS_Point(sg.Point(10, 48), dt.datetime(2017, 07, 25, 20, 0, 0), pyproj.Proj(init="epsg:4326"))], self.ip1)])
        mc2.reproject(pyproj.Proj(init="epsg:32631"))
        self.assertEqual(mc2.crs.srs, pyproj.Proj(init="epsg:32631").srs)
        self.assertEqual(mc2.moving_list[0].crs.srs, pyproj.Proj(init="epsg:32631").srs)
        
        
class Test_Moving_Polygon(unittest.TestCase):
    
    def setUp(self):
        
        self.tsu1 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.ip = zeit.Interpolator([self.tsu1])
        
        self.tslr1 = mg.TS_LinearRing(sg.LinearRing([(1,0),(3,0),(3,3),(1,3),(1,0)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tslr2 = mg.TS_LinearRing(sg.LinearRing([(3,0),(5,0),(5,3),(3,3),(3,0)]), dt.datetime(2017, 07, 25, 20, 0, 10))
        
        self.tslr3 = mg.TS_LinearRing(sg.LinearRing([(1.5,1),(2.5,1),(2.5,2),(1.5,2),(1.5,1)]), dt.datetime(2017, 07, 25, 20, 0, 2))
        self.tslr4 = mg.TS_LinearRing(sg.LinearRing([(3.5,1),(4.5,1),(4.5,2),(3.5,2),(3.5,1)]), dt.datetime(2017, 07, 25, 20, 0, 15))
        
        self.mlr1 = mg.Moving_LinearRing([self.tslr1, self.tslr2], self.ip)
        self.mlr2 = mg.Moving_LinearRing([self.tslr3, self.tslr4], self.ip)
    
    def test_init(self):
        
        # test if TypeError is raised if type of exterior_ring or interior_rings is not sptemp.moving_geometry.Moving_LinearRing
        with self.assertRaises(TypeError):
            mg.Moving_Polygon(self.tslr1, [self.mlr2])
            
        with self.assertRaises(TypeError):
            mg.Moving_Polygon(self.mlr1, self.mlr2)
        
        with self.assertRaises(TypeError):
            mg.Moving_Polygon(self.mlr1, [self.tslr3])
            
            
    def test_interpolate(self):
        
        mlp = mg.Moving_Polygon(self.mlr1, [self.mlr2])
        
        t1 = dt.datetime(2017, 07, 25, 19, 0, 2)
        t2 = dt.datetime(2017, 07, 25, 20, 0, 1)
        t3 = dt.datetime(2017, 07, 25, 20, 0, 5)
        t4 = dt.datetime(2017, 07, 25, 20, 0, 12)
        
        # test if TypeError is raised if time is not of type datetime.datetime
        with self.assertRaises(TypeError):
            mlp.interpolate(123)
            
        # test if TypeError is raised if args_dict is not of type dict
        with self.assertRaises(TypeError):
            mlp.interpolate(dt.datetime(2017, 07, 25, 20, 0, 2), [123])
            
        # test if correct values are returned
        mlp_t1 = mlp.interpolate(t1)
        self.assertEqual(mlp_t1, None)
        
        mlp_t2 = mlp.interpolate(t2)
        self.assertTrue(isinstance(mlp_t2, mg.TS_Geometry))
        self.assertEqual(len(mlp_t2.value.interiors[:]), 0)
        self.assertEqual(mlp_t2.value.exterior, sg.LinearRing([(1,0),(3,0),(3,3),(1,3),(1,0)]))
        
        mlp_t3 = mlp.interpolate(t3)
        self.assertEqual(len(mlp_t3.value.interiors[:]), 1)
        self.assertEqual(mlp_t3.value.interiors[0], sg.LinearRing([(1.5,1),(2.5,1),(2.5,2),(1.5,2),(1.5,1)]))
        
        mlp_t4 = mlp.interpolate(t4)
        self.assertEqual(mlp_t4, None)
        
    def test_slice(self):
        
        mlp = mg.Moving_Polygon(self.mlr1, [self.mlr2])
        
        s_time = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 7))
        
        # test if TypeError is raised if time not of type sptemp.zeit.TimePeriod
        with self.assertRaises(TypeError):
            mlp.slice(123)
            
        # test if correct value is returned
        m_sl1 = mlp.slice(s_time)
        self.assertEqual(len(m_sl1.interior_rings), 1)
        
    def test_resampled_slice(self):
        
        mlp = mg.Moving_Polygon(self.mlr1, [self.mlr2])
        mlp_reslice = mlp.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 7), dt.datetime(2017, 07, 25, 20, 0, 15)])
        self.assertEqual(len(mlp_reslice.exterior_ring), 2)
        self.assertEqual(len(mlp_reslice.interior_rings), 1)
        self.assertEqual(len(mlp_reslice.interior_rings[0]), 2)
        self.assertTrue(isinstance(mlp_reslice, mg.Moving_Polygon))
        
    def test_start_time(self):
        
        mlp = mg.Moving_Polygon(self.mlr1, [self.mlr2])
        self.assertEqual(mlp.start_time(), dt.datetime(2017, 07, 25, 20, 0, 0))
        
    def test_end_time(self):
        
        mlp = mg.Moving_Polygon(self.mlr1, [self.mlr2])
        self.assertEqual(mlp.end_time(), dt.datetime(2017, 07, 25, 20, 0, 10))
        
    def test_reproject(self):
         
        mlp = mg.Moving_Polygon(self.mlr1, [self.mlr2])
         
        # test if ValueError is raised if self.crs is None
        with self.assertRaises(ValueError):
            mlp.reproject(pyproj.Proj(init="epsg:32631"))
             
        # test if Moving_Polygon is reprojected correctly
        mlp2 = mg.Moving_Polygon(mg.Moving_LinearRing([
            mg.TS_LinearRing(sg.LinearRing([(10.1,48),(10.3,48),(10.3,48.3),(10.11,48.3),(10.1,48)]),
                             dt.datetime(2017, 07, 25, 20, 0, 0),
                             pyproj.Proj(init="epsg:4326"))], self.ip),
            [mg.Moving_LinearRing([mg.TS_LinearRing(sg.LinearRing([(10.15,48.1),(10.25,48.1),(10.25,48.2),(10.15,48.2),(10.15,48.1)]),
                                                    dt.datetime(2017, 07, 25, 20, 0, 2),
                                                    pyproj.Proj(init="epsg:4326"))], self.ip)])
         
        mlp2.reproject(pyproj.Proj(init="epsg:32631"))
        self.assertEqual(mlp2.exterior_ring.crs.srs, pyproj.Proj(init="epsg:32631").srs)
        self.assertEqual(mlp2.interior_rings[0].crs.srs, pyproj.Proj(init="epsg:32631").srs)
        
        
class Test_Moving_MultiPoint(unittest.TestCase):
    
    def setUp(self):
        
        self.tsu1 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.tsu2 = zeit.TS_Unit(IPoint.linear_point, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.ip1 = zeit.Interpolator([self.tsu1])
        self.ip2 = zeit.Interpolator([self.tsu2])
        
        self.tsp1 = mg.TS_Point(sg.Point(1,1), dt.datetime(2017, 07, 25, 20, 0, 5))
        self.tsp2 = mg.TS_Point(sg.Point(2,1), dt.datetime(2017, 07, 25, 20, 0, 15))
        
        self.tsp3 = mg.TS_Point(sg.Point(5,1), dt.datetime(2017, 07, 25, 20, 0, 10))
        self.tsp4 = mg.TS_Point(sg.Point(2,1), dt.datetime(2017, 07, 25, 20, 0, 20))
        
        self.mp1 = mg.Moving_Point([self.tsp1, self.tsp2], self.ip2)
        self.mp2 = mg.Moving_Point([self.tsp3, self.tsp4], self.ip1)
        
    def test_init(self):
        
        # test if ValueError is raised if moving_list is empty
        with self.assertRaises(ValueError):
            mg.Moving_MultiPoint([])
        
        # test if TypeError is raised if type of moving_list is not list
        with self.assertRaises(TypeError):
            mg.Moving_MultiPoint(self.mp1)
            
        # test if TypeError is raised if moving_list contains objects not of type Moving_Point
        with self.assertRaises(TypeError):
            mg.Moving_MultiPoint([self.mp1, zeit.Moving_Object([self.tsp3, self.tsp4], self.ip1)])
        
    def test_interpolate(self):
        
        mmp = mg.Moving_MultiPoint([self.mp1, self.mp2])
        
        # test if correct value is returned
        mmp_t1 = mmp.interpolate(dt.datetime(2017, 07, 25, 20, 0, 0))
        self.assertEqual(mmp_t1, None)
        
        mmp_t2 = mmp.interpolate(dt.datetime(2017, 07, 25, 20, 0, 10))
        self.assertTrue(isinstance(mmp_t2, mg.TS_Geometry))
        self.assertTrue(isinstance(mmp_t2.value, sg.MultiPoint))
        self.assertEqual(mmp_t2.value[0], sg.Point(1.5,1))
        self.assertEqual(mmp_t2.value[1], sg.Point(5,1))
        
    def test_slice(self):
        
        mmp = mg.Moving_MultiPoint([self.mp1, self.mp2])
        
        s_time = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 15))
        
        # test if TypeError is raised if time not of type sptemp.zeit.TimePeriod
        with self.assertRaises(TypeError):
            mmp.slice(123)
            
        # test if correct value is returned
        m_sl1 = mmp.slice(s_time)
        self.assertEqual(len(m_sl1.moving_list), 2)
        
    def test_resampled_slice(self):
        
        mmp = mg.Moving_MultiPoint([self.mp1, self.mp2])
        mmp_reslice = mmp.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 4), dt.datetime(2017, 07, 25, 20, 0, 8)])
        self.assertEqual(len(mmp_reslice.moving_list), 1)
        self.assertEqual(len(mmp_reslice.moving_list[0]), 2)
        self.assertTrue(isinstance(mmp_reslice, mg.Moving_MultiPoint))
        
        
class Test_Moving_MultiLineString(unittest.TestCase):
    
    def setUp(self):
        
        self.tsu1 = zeit.TS_Unit(ICurve.basic_linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.ip1 = zeit.Interpolator([self.tsu1])
        
        self.tsl1 = mg.TS_LineString(sg.LineString([(2,0),(1,1),(2,2)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tsl2 = mg.TS_LineString(sg.LineString([(4,0),(5,1)]), dt.datetime(2017, 07, 25, 20, 0, 10))
        
        self.tsl3 = mg.TS_LineString(sg.LineString([(7,0),(7,4)]), dt.datetime(2017, 07, 25, 20, 0, 5))
        self.tsl4 = mg.TS_LineString(sg.LineString([(8,0),(7,2)]), dt.datetime(2017, 07, 25, 20, 0, 15))
        
        self.ml1 = mg.Moving_LineString([self.tsl1, self.tsl2], self.ip1)
        self.ml2 = mg.Moving_LineString([self.tsl3, self.tsl4], self.ip1)
        
    def test_init(self):
        
        # test if ValueError is raised if moving_list is empty
        with self.assertRaises(ValueError):
            mg.Moving_MultiLineString([])
        
        # test if TypeError is raised if type of moving_list is not list
        with self.assertRaises(TypeError):
            mg.Moving_MultiLineString(self.ml1)
            
        # test if TypeError is raised if moving_list contains objects not of type Moving_Point
        with self.assertRaises(TypeError):
            mg.Moving_MultiPoint([self.ml1, zeit.Moving_Object([self.tsl3, self.tsl4], self.ip1)])
            
    def test_interpolate(self):
        
        mml = mg.Moving_MultiLineString([self.ml1, self.ml2])
        
        # test if correct value is returned
        mml_t1 = mml.interpolate(dt.datetime(2017, 07, 25, 20, 0, 20))
        self.assertEqual(mml_t1, None)
        
        mml_t2 = mml.interpolate(dt.datetime(2017, 07, 25, 20, 0, 5))
        self.assertTrue(isinstance(mml_t2, mg.TS_Geometry))
        self.assertTrue(isinstance(mml_t2.value, sg.MultiLineString))
        self.assertEqual(mml_t2.value[0], sg.LineString([(3.0, 0.0), (2.75, 0.75), (3.5, 1.5)]))
        self.assertEqual(mml_t2.value[1], sg.LineString([(7,0),(7,4)]))
        
    def test_slice(self):
        
        mml = mg.Moving_MultiLineString([self.ml1, self.ml2])
        
        s_time = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 4))
        
        # test if TypeError is raised if time not of type sptemp.zeit.TimePeriod
        with self.assertRaises(TypeError):
            mml.slice(123)
            
        # test if correct value is returned
        m_sl1 = mml.slice(s_time)
        self.assertEqual(len(m_sl1.moving_list), 1)
        self.assertEqual(m_sl1.moving_list[0][0].value, sg.LineString([(2,0),(1,1),(2,2)]))
        
    def test_resampled_slice(self):
        
        mml = mg.Moving_MultiLineString([self.ml1, self.ml2])
        mml_reslice = mml.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 4), dt.datetime(2017, 07, 25, 20, 0, 8)])
        self.assertEqual(len(mml_reslice.moving_list), 2)
        self.assertEqual(len(mml_reslice.moving_list[0]), 2)
        self.assertTrue(isinstance(mml_reslice, mg.Moving_MultiLineString))
        
        
class Test_Moving_MultiPolygon(unittest.TestCase):
    
    def setUp(self):
        
        self.tsu1 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.ip = zeit.Interpolator([self.tsu1])
        
        self.tslr1 = mg.TS_LinearRing(sg.LinearRing([(1,0),(3,0),(3,3),(1,3),(1,0)]), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.tslr2 = mg.TS_LinearRing(sg.LinearRing([(3,0),(5,0),(5,3),(3,3),(3,0)]), dt.datetime(2017, 07, 25, 20, 0, 10))
        
        self.tslr3 = mg.TS_LinearRing(sg.LinearRing([(11,10),(13,10),(13,13),(11,13),(11,10)]), dt.datetime(2017, 07, 25, 20, 0, 2))
        self.tslr4 = mg.TS_LinearRing(sg.LinearRing([(13,10),(15,10),(15,13),(13,13),(13,10)]), dt.datetime(2017, 07, 25, 20, 0, 15))
        
        self.mlr1 = mg.Moving_LinearRing([self.tslr1, self.tslr2], self.ip)
        self.mlr2 = mg.Moving_LinearRing([self.tslr3, self.tslr4], self.ip)
        
        self.mpl1 = mg.Moving_Polygon(self.mlr1)
        self.mpl2 = mg.Moving_Polygon(self.mlr2)
        
    def test_init(self):
        
        # test if ValueError is raised if moving_list is empty
        with self.assertRaises(ValueError):
            mg.Moving_MultiPolygon([])
        
        # test if TypeError is raised if type of moving_list is not list
        with self.assertRaises(TypeError):
            mg.Moving_MultiPolygon(self.mpl1)
            
        # test if TypeError is raised if moving_list contains objects not of type Moving_Point
        with self.assertRaises(TypeError):
            mg.Moving_MultiPoint([self.mpl1, zeit.Moving_Object([self.tslr1, self.tslr2], self.ip)])
            
    def test_interpolate(self):
        
        mmpl = mg.Moving_MultiPolygon([self.mpl1, self.mpl2])
        
        # test if correct value is returned
        mmpl_t1 = mmpl.interpolate(dt.datetime(2017, 07, 25, 20, 0, 25))
        self.assertEqual(mmpl_t1, None)
        
        mmpl_t2 = mmpl.interpolate(dt.datetime(2017, 07, 25, 20, 0, 12))
        self.assertTrue(isinstance(mmpl_t2, mg.TS_Geometry))
        self.assertTrue(isinstance(mmpl_t2.value, sg.MultiPolygon))
        self.assertEqual(len(mmpl_t2.value), 1)
        self.assertEqual(mmpl_t2.value[0], sg.Polygon([(11,10),(13,10),(13,13),(11,13),(11,10)]))
        
    def test_slice(self):
        
        mmpl = mg.Moving_MultiPolygon([self.mpl1, self.mpl2])
        
        s_time = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 10))
        
        # test if TypeError is raised if time not of type sptemp.zeit.TimePeriod
        with self.assertRaises(TypeError):
            mmpl.slice(123)
            
        # test if TypeError is raised if interpolator_dict not of type dict
        with self.assertRaises(TypeError):
            mmpl.slice(s_time, [self.ip.slice(s_time)])
            
        # test if correct value is returned
        m_sl1 = mmpl.slice(s_time)
        self.assertTrue(isinstance(m_sl1, mg.Moving_MultiPolygon))
        self.assertEqual(len(m_sl1.moving_list), 1)
        self.assertEqual(m_sl1.moving_list[0].exterior_ring[0].value, sg.LinearRing([(3,0),(5,0),(5,3),(3,3),(3,0)]))
        
    def test_resampled_slice(self):
        
        mmpl = mg.Moving_MultiPolygon([self.mpl1, self.mpl2])
        mmpl_reslice = mmpl.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 4), dt.datetime(2017, 07, 25, 20, 0, 8)])
        self.assertEqual(len(mmpl_reslice.moving_list), 2)
        self.assertTrue(isinstance(mmpl_reslice, mg.Moving_MultiPolygon))



unittest.main()       