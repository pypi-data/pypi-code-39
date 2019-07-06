# -*- coding: utf-8 -*-
"""
This module contains the unit-tests for the sptemp.zeit-modul

Todo:
 
"""
import unittest
import datetime as dt

from sptemp import zeit
from sptemp.interpolation import ICollection as IC


class Test_Time_Period(unittest.TestCase):
    
    def setUp(self):
        self.tp1 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 20), dt.datetime(2018, 07, 25, 18, 30, 40))
        self.tp2 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 30), dt.datetime(2018, 07, 25, 18, 30, 32))
        self.tp3 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 50), dt.datetime(2018, 07, 25, 18, 30, 55))
        
    def test_init(self):
        
        # test if TypeError is raised when start or end is not of type 'datetime.datetime'
        with self.assertRaises(TypeError):
            zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 20), "2018, 07, 25, 18, 30, 20")
        
        with self.assertRaises(TypeError):
            zeit.Time_Period(123.5, dt.datetime(2018, 07, 25, 18, 30, 20))
            
        # test if ValueError is raised when start >= end
        with self.assertRaises(ValueError):
            zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 20), dt.datetime(2018, 07, 25, 18, 30, 20))
            
    def test_start(self):
        
        # test if correct value is returned
        self.assertEqual(self.tp1.start, dt.datetime(2018, 07, 25, 18, 30, 20))
        
        # test if TypeError is raised when start is not of type 'datetime.datetime'
        with self.assertRaises(TypeError):
            self.tp1.start = "xy"
            
        # test if ValueError is raised when start >= end
        with self.assertRaises(ValueError):
            self.tp1.start = dt.datetime(2018, 07, 25, 18, 30, 45)
            
        # test if correct value is assigned
        self.tp1.start = dt.datetime(2018, 07, 25, 18, 30, 29)
        self.assertEqual(self.tp1.start, dt.datetime(2018, 07, 25, 18, 30, 29))
        
    def test_end(self):
        
        # test if correct value is returned
        self.assertEqual(self.tp1.end, dt.datetime(2018, 07, 25, 18, 30, 40))
        
        # test if TypeError is raised when end is not of type 'datetime.datetime'
        with self.assertRaises(TypeError):
            self.tp1.end = "xy"
        
        # test if ValueError is raised when start >= end
        with self.assertRaises(ValueError):
            self.tp1.end = dt.datetime(2018, 07, 25, 18, 30, 20)
            
        # test if correct value is assigned
        self.tp1.end = dt.datetime(2018, 07, 25, 18, 30, 50)
        self.assertEqual(self.tp1.end, dt.datetime(2018, 07, 25, 18, 30, 50))
        
    def test_from_iso(self):
        
        tp1 = zeit.Time_Period.from_iso("2017-07-25T22:00:00", "2017-07-25T22:00:10")
        self.assertEqual(tp1, zeit.Time_Period(dt.datetime(2017, 7, 25, 22, 0, 0), dt.datetime(2017, 7, 25, 22, 0, 10)))
        
    def test_lt(self):
        
        # test if TypeError is raised if type != datetime.datetime or sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            self.tp1 < "xy"
        
        ts_x = dt.datetime(2018, 07, 25, 18, 30, 40)
        tp_x = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 32), dt.datetime(2018, 07, 25, 18, 30, 34))
        tp_x2 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 34), dt.datetime(2018, 07, 25, 18, 30, 36))
        
        # type(another) = datetime.datetime
        self.assertTrue(tp_x < ts_x)
        self.assertFalse(self.tp1 < ts_x)
        
        # type(another) = sptemp.zeit.Time_Period
        self.assertTrue(self.tp2 < self.tp3)
        self.assertFalse(self.tp2 < tp_x)
        self.assertFalse(tp_x < tp_x2)
        
    def test_gt(self):
        
        # test if TypeError is raised if type != datetime.datetime or sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            self.tp1 > "xy"
            
        tp_x = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 32), dt.datetime(2018, 07, 25, 18, 30, 34))
        tp_x2 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 34), dt.datetime(2018, 07, 25, 18, 30, 36))
        
        # type(another) = datetime.datetime
        self.assertTrue(tp_x2 > tp_x.start)
        self.assertFalse(tp_x2 > tp_x.end)
        
        # type(another) = sptemp.zeit.Time_Period
        self.assertTrue(self.tp3 > self.tp1)
        self.assertFalse(tp_x2 > tp_x)
        
    def test_eq(self):
        tp_x = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 20), dt.datetime(2018, 07, 25, 18, 30, 40))
        
        self.assertTrue(self.tp1 == tp_x)
        self.assertFalse(self.tp1 == self.tp2)
        self.assertFalse(self.tp1 == 123)
        
    def test_ne(self):
        tp_x = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 20), dt.datetime(2018, 07, 25, 18, 30, 40))
        
        self.assertFalse(self.tp1 != tp_x)
        self.assertTrue(self.tp1 != self.tp2)
        self.assertTrue(self.tp1 != 123)
        
    def test_before(self):
        
        # test if TypeError is raised if type != datetime.datetime or sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            self.tp1.before("xy")
        
        ts_x = dt.datetime(2018, 07, 25, 18, 30, 40)
        tp_x = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 32), dt.datetime(2018, 07, 25, 18, 30, 34))
        tp_x2 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 34), dt.datetime(2018, 07, 25, 18, 30, 36))
        
        # type(another) = datetime.datetime
        self.assertTrue(tp_x.before(ts_x))
        self.assertFalse(self.tp1.before(ts_x))
        
        # type(another) = sptemp.zeit.Time_Period
        self.assertTrue(self.tp2.before(self.tp3))
        self.assertFalse(self.tp2.before(tp_x))
        self.assertFalse(tp_x.before(tp_x2))
        
    def test_after(self):
        
        # test if TypeError is raised if type != datetime.datetime or sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            self.tp1.after("xy")
            
        tp_x = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 32), dt.datetime(2018, 07, 25, 18, 30, 34))
        tp_x2 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 34), dt.datetime(2018, 07, 25, 18, 30, 36))
        
        # type(another) = datetime.datetime
        self.assertTrue(tp_x2.after(tp_x.start))
        self.assertFalse(tp_x2.after(tp_x.end))
        
        # type(another) = sptemp.zeit.Time_Period
        self.assertTrue(self.tp3.after(self.tp1))
        self.assertFalse(tp_x2.after(tp_x))
        
    def test_contains(self):
        
        # test if TypeError is raised if type != datetime.datetime or sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            self.tp1.contains("xy")
            
        ts_x1 = dt.datetime(2018, 07, 25, 18, 30, 40)
        ts_x2 = dt.datetime(2018, 07, 25, 18, 30, 50)
        tp_x1 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 39), dt.datetime(2018, 07, 25, 18, 30, 50))
        tp_x2 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 40), dt.datetime(2018, 07, 25, 18, 30, 45))
        tp_x3 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 40), dt.datetime(2018, 07, 25, 18, 30, 44))
            
        # type(another) = datetime.datetime
        self.assertTrue(tp_x1.contains(ts_x1))
        self.assertFalse(tp_x1.contains(ts_x2))
        self.assertFalse(tp_x2.contains(ts_x1))
        self.assertFalse(tp_x2.contains(ts_x2))
        
        # type(another) = sptemp.zeit.Time_Period
        self.assertTrue(tp_x1.contains(tp_x2))
        self.assertFalse(tp_x2.contains(tp_x1))
        self.assertFalse(tp_x2.contains(tp_x3))
        
    def test_includes(self):
        
        # test if TypeError is raised if type != datetime.datetime or sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            self.tp1.includes("xy")
            
        ts_x1 = dt.datetime(2018, 07, 25, 18, 30, 39)
        ts_x2 = dt.datetime(2018, 07, 25, 18, 30, 50)
        ts_x3 = dt.datetime(2018, 07, 25, 18, 30, 45)
        tp_x1 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 39), dt.datetime(2018, 07, 25, 18, 30, 50))
        tp_x2 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 40), dt.datetime(2018, 07, 25, 18, 30, 45))
        tp_x3 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 40), dt.datetime(2018, 07, 25, 18, 30, 44))
            
        # type(another) = datetime.datetime
        self.assertTrue(tp_x1.includes(ts_x1))
        self.assertTrue(tp_x1.includes(ts_x2))
        self.assertTrue(tp_x1.includes(ts_x3))
        self.assertFalse(tp_x2.includes(ts_x1))
        self.assertFalse(tp_x2.includes(ts_x2))
        
        # type(another) = sptemp.zeit.Time_Period
        self.assertTrue(tp_x2.includes(tp_x3))
        self.assertTrue(tp_x1.includes(tp_x3))
        self.assertFalse(tp_x3.includes(tp_x1))
        
    def test_meets(self):
        
        # test if TypeError is raised if type != datetime.datetime or sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            self.tp1.meets("xy")
            
        ts_x1 = dt.datetime(2018, 07, 25, 18, 30, 40)
        tp_x1 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 30), dt.datetime(2018, 07, 25, 18, 30, 40))
        tp_x2 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 40), dt.datetime(2018, 07, 25, 18, 30, 45))
        
        # type(another) = datetime.datetime
        self.assertTrue(tp_x1.meets(ts_x1))
        self.assertFalse(tp_x2.meets(ts_x1))
        
        # type(another) = sptemp.zeit.Time_Period
        self.assertTrue(tp_x1.meets(tp_x2))
        self.assertFalse(tp_x2.meets(tp_x1))
        
    def test_metBy(self):
        
        # test if TypeError is raised if type != datetime.datetime or sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            self.tp1.metBy("xy")
            
        ts_x1 = dt.datetime(2018, 07, 25, 18, 30, 30)
        tp_x1 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 30), dt.datetime(2018, 07, 25, 18, 30, 40))
        tp_x2 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 20), dt.datetime(2018, 07, 25, 18, 30, 30))
        
        # type(another) = datetime.datetime
        self.assertTrue(tp_x1.metBy(ts_x1))
        self.assertFalse(tp_x2.metBy(ts_x1))
        
        # type(another) = sptemp.zeit.Time_Period
        self.assertTrue(tp_x1.metBy(tp_x2))
        self.assertFalse(tp_x2.metBy(tp_x1))
        
    def test_equals(self):
        
        # test if TypeError is raised if type != sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            self.tp1.equals(dt.datetime(2018, 07, 25, 18, 30, 40))
        
        tp_x = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 20), dt.datetime(2018, 07, 25, 18, 30, 40))
        
        self.assertTrue(self.tp1.equals(tp_x))
        self.assertFalse(self.tp1.equals(self.tp2))
            
    def test_during(self):
        
        # test if TypeError is raised if type != sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            self.tp1.during(dt.datetime(2018, 07, 25, 18, 30, 40))
            
        tp_x1 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 39), dt.datetime(2018, 07, 25, 18, 30, 50))
        tp_x2 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 40), dt.datetime(2018, 07, 25, 18, 30, 45))
        tp_x3 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 40), dt.datetime(2018, 07, 25, 18, 30, 44))
        
        self.assertTrue(tp_x2.during(tp_x1))
        self.assertFalse(tp_x3.during(tp_x2))
        self.assertFalse(tp_x1.during(tp_x3))
        
    def test_overlaps(self):
        
        # test if TypeError is raised if type != sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            self.tp1.overlaps(dt.datetime(2018, 07, 25, 18, 30, 40))
            
        tp_x1 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 40), dt.datetime(2018, 07, 25, 18, 30, 50))
        tp_x2 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 45), dt.datetime(2018, 07, 25, 18, 30, 55))
        tp_x3 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 50), dt.datetime(2018, 07, 25, 18, 30, 55))
        tp_x4 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 44), dt.datetime(2018, 07, 25, 18, 30, 46))
        tp_x5 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 35), dt.datetime(2018, 07, 25, 18, 30, 46))
        
        self.assertTrue(tp_x1.overlaps(tp_x2))
        self.assertFalse(tp_x1.overlaps(tp_x3))
        self.assertFalse(tp_x1.overlaps(tp_x4))
        self.assertFalse(tp_x1.overlaps(tp_x5))
        
    def test_overlappedBy(self):
        
        # test if TypeError is raised if type != sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            self.tp1.overlappedBy(dt.datetime(2018, 07, 25, 18, 30, 40))
            
        tp_x1 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 40), dt.datetime(2018, 07, 25, 18, 30, 50))
        tp_x2 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 45), dt.datetime(2018, 07, 25, 18, 30, 55))
        tp_x3 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 50), dt.datetime(2018, 07, 25, 18, 30, 55))
        tp_x4 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 44), dt.datetime(2018, 07, 25, 18, 30, 46))
        tp_x5 = zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 35), dt.datetime(2018, 07, 25, 18, 30, 46))
        
        self.assertTrue(tp_x1.overlappedBy(tp_x5))
        self.assertFalse(tp_x1.overlappedBy(tp_x3))
        self.assertFalse(tp_x1.overlappedBy(tp_x4))
        self.assertFalse(tp_x1.overlappedBy(tp_x2))
            
class Test_TS_Object(unittest.TestCase):
    
    def setUp(self):
        
        self.ts1 = zeit.TS_Object(10, dt.datetime(2018, 07, 25, 18, 30, 10))
        self.ts2 = zeit.TS_Object(20, zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 20), dt.datetime(2018, 07, 25, 18, 30, 40)))
        
    def test_init(self):
        
        # test if TypeError is raised when ts is not of type datetime.datetime and ts is not of type Time_Period
        with self.assertRaises(TypeError):
            zeit.TS_Object(123, "xy")
            
    def test_value(self):
        
        self.assertEqual(self.ts1.value, 10)
        
        # test if TypeError is raised when wrong type is assigned
        with self.assertRaises(TypeError):
            self.ts2.value = "xy"
        
        # check if correct value is assigned
        self.ts1.value = 14
        self.assertEqual(self.ts1.value, 14)
        
    def test_eq(self):
        
        ts_x1 = zeit.TS_Object(10, dt.datetime(2018, 07, 25, 18, 30, 10))
        ts_x2 = zeit.TS_Object(20, zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 20), dt.datetime(2018, 07, 25, 18, 30, 40)))
        
        self.assertTrue(self.ts1 == ts_x1)
        self.assertTrue(self.ts2 == ts_x2)
        self.assertFalse(ts_x1 == ts_x2)
        self.assertFalse(ts_x1 == zeit.TS_Object(20, dt.datetime(2018, 07, 25, 18, 30, 10)))
        self.assertFalse(ts_x1 == zeit.TS_Object(10, dt.datetime(2017, 07, 25, 18, 30, 10)))
        
    def test_ne(self):
        
        ts_x1 = zeit.TS_Object(10, dt.datetime(2018, 07, 25, 18, 30, 10))
        ts_x2 = zeit.TS_Object(20, zeit.Time_Period(dt.datetime(2018, 07, 25, 18, 30, 20), dt.datetime(2018, 07, 25, 18, 30, 40)))
        
        self.assertFalse(self.ts1 != ts_x1)
        self.assertFalse(self.ts2 != ts_x2)
        self.assertTrue(ts_x1 != ts_x2)
        self.assertTrue(ts_x1 != zeit.TS_Object(20, dt.datetime(2018, 07, 25, 18, 30, 10)))
        self.assertTrue(ts_x1 != zeit.TS_Object(10, dt.datetime(2017, 07, 25, 18, 30, 10)))
        
    def test_start_time(self):
        
        self.assertEqual(self.ts1.start_time(), dt.datetime(2018, 07, 25, 18, 30, 10))
        self.assertEqual(self.ts2.start_time(), dt.datetime(2018, 07, 25, 18, 30, 20))
        
    def test_end_time(self):
        
        self.assertEqual(self.ts1.end_time(), dt.datetime(2018, 07, 25, 18, 30, 10))
        self.assertEqual(self.ts2.end_time(), dt.datetime(2018, 07, 25, 18, 30, 40))
        
        
class Test_TS_Unit(unittest.TestCase):
    
    def setUp(self):
        self.start_ts1 = zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 0))
        self.start_ts2 = zeit.TS_Object(10.0, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.start_ts3 = zeit.TS_Object("test", dt.datetime(2017, 07, 25, 20, 0, 0))
        
        self.end_ts1 = zeit.TS_Object(20, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.end_ts2 = zeit.TS_Object(20.0, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.end_ts3 = zeit.TS_Object("xy", dt.datetime(2017, 07, 25, 20, 0, 30))
    
    def test_init(self):
        # test if TypeError is raised when ts is not of type sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            zeit.TS_Unit(IC.constant, dt.datetime(2018, 07, 25, 18, 30, 10))
        
        # test if TypeError is raised when value is not of type types.functionType
        with self.assertRaises(TypeError):
            zeit.TS_Unit(123, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
            
        tu1 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        
        self.assertEqual(tu1.value, IC.constant)
        self.assertEqual(tu1.ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        
    def test_interpolate(self):
        
        tu1 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 55)))
        tu2 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 55)))
        tu3 = zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 55)))
        
        # test if TypeError is raised if start_ts or end_ts is not of type sptemp.zeit.TS_Object
        with self.assertRaises(TypeError):
            tu1.interpolate("xy", self.end_ts2, dt.datetime(2017, 07, 25, 20, 0, 12))
            
        with self.assertRaises(TypeError):
            tu1.interpolate(self.start_ts2, "xy", dt.datetime(2017, 07, 25, 20, 0, 12))
            
        # test if TypeError is raised if time is not of type datetime.datetime
        with self.assertRaises(TypeError):
            tu1.interpolate(self.start_ts2, self.end_ts2, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 55)))
            
        # test if ValueError is raised if Time_Unit does not include start_ts.end_time() or time
        with self.assertRaises(ValueError):
            tu1.interpolate(zeit.TS_Object(10, dt.datetime(2017, 07, 25, 19, 0, 0)), self.end_ts1, dt.datetime(2017, 07, 25, 20, 0, 12))
            
        with self.assertRaises(ValueError):
            tu1.interpolate(self.start_ts1, self.end_ts1, dt.datetime(2017, 07, 25, 19, 0, 12))
            
        self.assertEqual(tu1.interpolate(self.start_ts1, self.end_ts1, dt.datetime(2017, 07, 25, 20, 0, 12)), zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 12)))
        self.assertEqual(tu2.interpolate(self.start_ts1, self.end_ts1, dt.datetime(2017, 07, 25, 20, 0, 12)), zeit.TS_Object(20, dt.datetime(2017, 07, 25, 20, 0, 12)))
        self.assertEqual(tu3.interpolate(self.start_ts1, self.end_ts1, dt.datetime(2017, 07, 25, 20, 0, 12)), zeit.TS_Object(16, dt.datetime(2017, 07, 25, 20, 0, 12)))
        
        
class Test_Interpolator(unittest.TestCase):
    
    def setUp(self):
        self.tsu1 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.tsu2 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.tsu3 = zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.tsu4 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 9), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.tsu5 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 12), dt.datetime(2017, 07, 25, 20, 0, 20)))
        
    def test_init(self):
        
        # test if ValueError is raised when ts_unit_list is empty
        with self.assertRaises(ValueError):
            zeit.Interpolator([])
            
        # test if TypeError is raised if ts_unit_list is not of type 'list'
        with self.assertRaises(TypeError):
            zeit.Interpolator("xy")
            
        # test if TypeError is raised if ts_unit_list includes objects that are not of type zeit.sptemp.TS_Unit
        with self.assertRaises(TypeError):
            zeit.Interpolator([self.tsu1, zeit.TS_Object(12, IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10))), self.tsu3])
            
        # test if TypeError is raised if ts_unit_list is not correctly time_sorted
        with self.assertRaises(ValueError):
            zeit.Interpolator([self.tsu1, self.tsu3, self.tsu2])
            
        with self.assertRaises(ValueError):
            zeit.Interpolator([self.tsu1, self.tsu4, self.tsu3])
        
        with self.assertRaises(ValueError):
            zeit.Interpolator([self.tsu1, self.tsu5, self.tsu3])
            
        # correct Interpolator object
        zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        
    def test_len(self):
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        self.assertEqual(len(ip), 3)
        del ip[0]
        self.assertEqual(len(ip), 2)
        
    def test_getitem(self):
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        self.assertEqual(ip[0], self.tsu1)
        self.assertEqual(ip[:2], [self.tsu1, self.tsu2])
        
    def test_setitem(self):
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        tsu_x = zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20)))
        
        # test if TypeError is raised if key is not of type int
        with self.assertRaises(TypeError):
            ip[0:2] = tsu_x
            
        # test if TypeError is raised if value is not of type sptemp.zeit.TS_Unit
        with self.assertRaises(TypeError):
            ip[1] = zeit.TS_Object(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20)))
            
        # test if IndexError is raised if Key is out of range
        with self.assertRaises(IndexError):
            ip[3] = tsu_x
            
        # test if ValueError is raised if value.ts does not match ts of replaced value
        with self.assertRaises(ValueError):
            ip[1] = zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 11), dt.datetime(2017, 07, 25, 20, 0, 20)))
            
        # correct assignment
        ip[1] = tsu_x
        self.assertEqual(ip.as_list(), [self.tsu1, tsu_x, self.tsu3])
        
    def test_delitem(self):
        
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        
        # test if ValueError is raised if key is not 0 AND key does not index last item of object
        with self.assertRaises(ValueError):
            del ip[1]
            
        with self.assertRaises(ValueError):
            del ip[0:2]
            
        # test if correct value is deleted
        del ip[0]
        self.assertEqual(ip.as_list(), [self.tsu2, self.tsu3])
        
        del ip[-1]
        self.assertEqual(ip.as_list(), [self.tsu2])
        
        # test if ValueError is raised if len(object) == 1
        with self.assertRaises(ValueError):
            del ip[0]
            
    def test_interpolate(self):
        
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        start_ts1 = zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 0))
        start_ts2 = zeit.TS_Object(10, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 5)))
        start_ts3 = zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 10))
        
        end_ts1 = zeit.TS_Object(20, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        end_ts2 = zeit.TS_Object(20, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 30)))
        end_ts3 = zeit.TS_Object(20, dt.datetime(2017, 07, 25, 20, 0, 30))
        
        # test if TypeError is raised if type of start_ts or end_ts is not sptemp.zeit.TS_Object
        with self.assertRaises(TypeError):
            ip.interpolate(123, end_ts1, dt.datetime(2017, 07, 25, 20, 0, 0))
            
        with self.assertRaises(TypeError):
            ip.interpolate(start_ts1, 123, dt.datetime(2017, 07, 25, 20, 0, 0))
            
        # test if TypeError is raised if time is not of type datetime.datetime
        with self.assertRaises(TypeError):
            ip.interpolate(start_ts1, end_ts1, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        
        # test if ValueError is raised if start_ts.end_time() < self.start_time
        with self.assertRaises(ValueError):
            ip.interpolate(zeit.TS_Object(10, dt.datetime(2017, 07, 25, 19, 0, 0)), end_ts1, dt.datetime(2017, 07, 25, 20, 0, 10))
         
        # test if ValueError is raised if time not between start_ts.end_time() and end_ts.start_time()
        with self.assertRaises(ValueError):
            ip.interpolate(start_ts1, end_ts1, dt.datetime(2017, 07, 25, 20, 0, 25))
            
        # test if ValueError is raised if start_ts.end_time() >= end_ts.start_time()
        with self.assertRaises(ValueError):
            ip.interpolate(start_ts1, start_ts1, dt.datetime(2017, 07, 25, 20, 0, 0))
            
        #print ip.interpolate(start_ts1, end_ts1, dt.datetime(2017, 07, 25, 20, 0, 15)).ts
        self.assertEqual(ip.interpolate(start_ts1, end_ts1, dt.datetime(2017, 07, 25, 20, 0, 15)), zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 15)))
        self.assertEqual(ip.interpolate(start_ts1, end_ts1, dt.datetime(2017, 07, 25, 20, 0, 10)), zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.assertEqual(ip.interpolate(start_ts1, end_ts1, dt.datetime(2017, 07, 25, 20, 0, 0)), zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 0)))
        
        self.assertEqual(ip.interpolate(start_ts2, end_ts2, dt.datetime(2017, 07, 25, 20, 0, 5)), zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 5)))
        self.assertEqual(ip.interpolate(start_ts2, end_ts2, dt.datetime(2017, 07, 25, 20, 0, 22)), zeit.TS_Object(14, dt.datetime(2017, 07, 25, 20, 0, 22)))
        self.assertEqual(ip.interpolate(start_ts2, end_ts2, dt.datetime(2017, 07, 25, 20, 0, 25)), zeit.TS_Object(20, dt.datetime(2017, 07, 25, 20, 0, 25)))
        
        self.assertEqual(ip.interpolate(start_ts3, end_ts3, dt.datetime(2017, 07, 25, 20, 0, 10)), zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.assertEqual(ip.interpolate(start_ts3, end_ts3, dt.datetime(2017, 07, 25, 20, 0, 30)), zeit.TS_Object(20, dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.assertEqual(ip.interpolate(start_ts3, end_ts3, dt.datetime(2017, 07, 25, 20, 0, 25)), zeit.TS_Object(15, dt.datetime(2017, 07, 25, 20, 0, 25)))
        self.assertEqual(ip.interpolate(start_ts3, end_ts3, dt.datetime(2017, 07, 25, 20, 0, 15)), zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 15)))
            
    def test_value(self):
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        
        # test if TypeError is raised if type of time is not datetime.datetime
        with self.assertRaises(TypeError):
            ip.value(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 11), dt.datetime(2017, 07, 25, 20, 0, 20)))
            
        # test if correct values are returned
        self.assertEqual(ip.value(dt.datetime(2017, 07, 25, 19, 0, 11)), [])
        self.assertEqual(ip.value(dt.datetime(2017, 07, 25, 20, 0, 31)), [])
        self.assertEqual(ip.value(dt.datetime(2017, 07, 25, 20, 0, 0)), [self.tsu1])
        self.assertEqual(ip.value(dt.datetime(2017, 07, 25, 20, 0, 5)), [self.tsu1])
        self.assertEqual(ip.value(dt.datetime(2017, 07, 25, 20, 0, 10)), [self.tsu1, self.tsu2])
        self.assertEqual(ip.value(dt.datetime(2017, 07, 25, 20, 0, 25)), [self.tsu3])
        self.assertEqual(ip.value(dt.datetime(2017, 07, 25, 20, 0, 30)), [self.tsu3])
        
    def test_slice(self):
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        
        # test if TypeError is raised if type of time is not sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            ip.slice(dt.datetime(2017, 07, 25, 20, 0, 20))
            
        tp1 = zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 59, 30), dt.datetime(2017, 07, 25, 20, 0, 5))
        tp2 = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 5))
        tp3 = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10))
        tp4 = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 15))
        tp5 = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 35))
        tp6 = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 30))
        tp7 = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 45))
        tp8 = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 31), dt.datetime(2017, 07, 25, 20, 0, 45))
        
        s1 = ip.slice(tp1)
        self.assertEqual(ip.start_time(), dt.datetime(2017, 07, 25, 20, 0, 0))
        self.assertEqual(len(s1), 1)
        self.assertEqual(s1[0], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 5))))
        
        s2 = ip.slice(tp2)
        self.assertEqual(len(s2), 1)
        self.assertEqual(s2[0], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 5))))
        
        s3 = ip.slice(tp3)
        self.assertEqual(len(s3), 1)
        self.assertEqual(s3[0], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10))))
        
        s4 = ip.slice(tp4)
        self.assertEqual(len(s4), 2)
        self.assertEqual(s4[0], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10))))
        self.assertEqual(s4[1], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 15))))
        
        s5 = ip.slice(tp5)
        self.assertEqual(len(s5), 1)
        self.assertEqual(s5[0], zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 30))))
        
        s6 = ip.slice(tp6)
        self.assertEqual(len(s6), 1)
        self.assertEqual(s6[0], zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 30))))
        
        s7 = ip.slice(tp7)
        self.assertEqual(len(s7), 2)
        self.assertEqual(s7[0], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20))))
        self.assertEqual(s7[1], zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30))))
        
        s8 = ip.slice(tp8)
        self.assertEqual(s8, None)
        
    def test_as_list(self):
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        self.assertEqual(ip.as_list(), [self.tsu1, self.tsu2, self.tsu3])
        
    def test_start_time(self):
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        self.assertEqual(ip.start_time(), dt.datetime(2017, 07, 25, 20, 0, 0))
        
    def test_end_time(self):
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        self.assertEqual(ip.end_time(), dt.datetime(2017, 07, 25, 20, 0, 30))
        
    def test_i_unit(self):
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        self.assertEqual(ip.i_unit(0), self.tsu1)
        
    def test_append(self):
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        tsu_x = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 30), dt.datetime(2017, 07, 25, 20, 0, 45)))
        
        # test if ValueError is raised if value is not of type sptemp.zeit.TS_Unit
        with self.assertRaises(TypeError):
            ip.append(zeit.TS_Object(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20))))
        
        # test if ValueError is raised if value is not of type sptemp.zeit.TS_Unit
        with self.assertRaises(ValueError):
            ip.append(self.tsu4)
            
        # check if correct value is assigned
        ip.append(tsu_x)
        self.assertEqual(len(ip), 4)
        self.assertEqual(ip[3], tsu_x)
        
    def test_insert(self):
        
        # test if Type Error is raised if value is not of type sptemp.zeit.TS_Unit
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        with self.assertRaises(TypeError):
            ip.insert(zeit.TS_Object(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20))))
            
        # test if ValueError is raised if value.start_time() and value.end_time() is not included in Time_Period(ip.start_time(), ip.end_time())
        with self.assertRaises(ValueError):
            ip.insert(zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 35), dt.datetime(2017, 07, 25, 20, 0, 45))))
            
        with self.assertRaises(ValueError):
            ip.insert(zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 0, 35), dt.datetime(2017, 07, 25, 19, 0, 45))))
            
        # test if value is correctly inserted
        tsu_x1 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 59, 30), dt.datetime(2017, 07, 25, 20, 0, 0)))
        tsu_x2 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 30), dt.datetime(2017, 07, 25, 20, 0, 40)))
        tsu_x3 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 59, 50), dt.datetime(2017, 07, 25, 20, 0, 5)))
        tsu_x4 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20)))
        tsu_x5 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 12), dt.datetime(2017, 07, 25, 20, 0, 16)))
        tsu_x6 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 25)))
        tsu_x7 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 35)))
        tsu_x8 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 25)))
        tsu_x9 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 45)))
        tsu_x10 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 45)))
        tsu_x11 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 25)))
        tsu_x12 = zeit.TS_Unit(IC.next_ts, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 45)))
        
        ip.insert(tsu_x1)
        self.assertEqual(len(ip), 4)
        self.assertEqual(ip[0], tsu_x1)
        del ip[0]
        
        ip.insert(tsu_x2)
        self.assertEqual(len(ip), 4)
        self.assertEqual(ip[-1], tsu_x2)
        del ip[-1]
        
        # -> replace to the left
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.insert(tsu_x3)
        self.assertEqual(len(ip), 4)
        self.assertEqual(ip[0], tsu_x3)
        self.assertEqual(ip[1], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 10))))
        
        # -> replace existing value
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.insert(tsu_x4)
        self.assertEqual(len(ip), 3)
        self.assertEqual(ip[1], tsu_x4)
        
        # -> split existing TS_Unit
        self.tsu2 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20)))
        sp_x1 = zeit.TS_Unit(self.tsu2.value, zeit.Time_Period(self.tsu2.start_time(), tsu_x5.start_time()))
        sp_x2 = zeit.TS_Unit(self.tsu2.value, zeit.Time_Period(tsu_x5.end_time(), self.tsu2.end_time()))
        
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.insert(tsu_x5)
        self.assertEqual(len(ip), 5)
        self.assertEqual(ip[2], tsu_x5)
        self.assertEqual(ip[1], sp_x1)
        self.assertEqual(ip[3], sp_x2)
        
        # adjust to the left--2
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.insert(tsu_x6)
        self.assertEqual(len(ip), 4)
        self.assertEqual(ip[2], tsu_x6)
        self.assertEqual(ip[3], zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 30))))
        
        # adjust to the right
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.insert(tsu_x7)
        self.assertEqual(len(ip), 4)
        self.assertEqual(ip[3], tsu_x7)
        self.assertEqual(ip[2], zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 25))))
        
        # adjust to the right and left
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.insert(tsu_x8)
        self.assertEqual(len(ip), 3)
        self.assertEqual(ip[1], tsu_x8)
        self.assertEqual(ip[0], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 5))))
        self.assertEqual(ip[2], zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 30))))
        
        # -> deleting multiple items without adjustment needed
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.insert(tsu_x9)
        self.assertEqual(len(ip), 2)
        self.assertEqual(ip[1], tsu_x9)
        self.assertEqual(ip[0], self.tsu1)
        
        # replace all items
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.insert(tsu_x10)
        self.assertEqual(len(ip), 1)
        self.assertEqual(ip[0], tsu_x10)
        
        # adjust to the left--3
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.insert(tsu_x11)
        self.assertEqual(len(ip), 2)
        self.assertEqual(ip[0], tsu_x11)
        self.assertEqual(ip[1], zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 30))))
        
        # adjust to the right--2
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.insert(tsu_x12)
        self.assertEqual(len(ip), 2)
        self.assertEqual(ip[1], tsu_x12)
        self.assertEqual(ip[0], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 5))))
    
    def test_delete(self):
        
        # test if TypeError is raised if time is not of type Time_Period
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        with self.assertRaises(TypeError):
            ip.delete(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20))
            
        # test if ValueError is raised if time would delete all items in Interpolator
        with self.assertRaises(ValueError):
            ip.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 30)))
            
        # test if ValueError is raised if time would delete values in the middle of the Interpolator
        with self.assertRaises(ValueError):
            ip.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 29)))
            
        tp1 = zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 59, 30), dt.datetime(2017, 07, 25, 20, 0, 5))
        tp2 = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 5))
        tp3 = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 15))
        tp4 = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 35))
        tp5 = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 30))
        tp6 = zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 45))
        
        # delete left
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.delete(tp1)
        self.assertEqual(len(ip), 3)
        self.assertEqual(ip[0], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 10))))
        
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.delete(tp2)
        self.assertEqual(len(ip), 3)
        self.assertEqual(ip[0], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 10))))
        
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.delete(tp3)
        self.assertEqual(len(ip), 2)
        self.assertEqual(ip[0], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 15), dt.datetime(2017, 07, 25, 20, 0, 20))))
        
        # delete right
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.delete(tp4)
        self.assertEqual(len(ip), 3)
        self.assertEqual(ip[2], zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 25))))
        
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.delete(tp5)
        self.assertEqual(len(ip), 3)
        self.assertEqual(ip[2], zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 25))))
        
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        ip.delete(tp6)
        self.assertEqual(len(ip), 1)
        self.assertEqual(ip[0], zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10))))
        
    def test_length(self):
        ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        self.assertEqual(ip.length(), 3)
        del ip[0]
        self.assertEqual(ip.length(), 2)
    

class Test_Moving_Object(unittest.TestCase):
    
    def setUp(self):
        self.tsu1 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.tsu2 = zeit.TS_Unit(IC.constant, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.tsu3 = zeit.TS_Unit(IC.linear, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.ip = zeit.Interpolator([self.tsu1, self.tsu2, self.tsu3])
        
        self.tpo1 = zeit.TS_Object(10, zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 0)))
        self.tpo2 = zeit.TS_Object(12, dt.datetime(2017, 07, 25, 20, 0, 5))
        self.tpo3 = zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 15)))
        self.tpo4 = zeit.TS_Object(18, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 19), dt.datetime(2017, 07, 25, 20, 0, 22)))
        self.tpo5 = zeit.TS_Object(20, dt.datetime(2017, 07, 25, 20, 0, 30))
        
    def test_init(self):
        
        # test if ValueError is raised if ts_object_list is empty
        with self.assertRaises(ValueError):
            zeit.Moving_Object([], self.ip)
            
        # test if ValueError is raised if ts_object_list is not of type list
        with self.assertRaises(TypeError):
            zeit.Moving_Object((self.tpo1, self.tpo2), self.ip)
            
        # test if ValueError is raised if interpolator is not of type sptemp.zeit.Interpolator
        with self.assertRaises(TypeError):
            zeit.Moving_Object([self.tpo1, self.tpo2], 123)
            
        # test if TypeError is raised if ts_object_list holds values that are not of type sptemp.zeit.TS_Object
        with self.assertRaises(TypeError):
            zeit.Moving_Object([self.tpo1, self.tpo2, 123], self.ip)
            
        # test if TypeError is raised if ts_object_list holds TS_Objects that don't hold the same type
        with self.assertRaises(TypeError):
            zeit.Moving_Object([self.tpo1, self.tpo2, zeit.TS_Object(20.0, dt.datetime(2017, 07, 25, 20, 0, 30))], self.ip)
            
        # test if ValueError is raised if ts_object_list is not sorted correctly and not disjoint
        with self.assertRaises(ValueError):
            zeit.Moving_Object([self.tpo1, self.tpo2, zeit.TS_Object(20, dt.datetime(2017, 07, 25, 20, 0, 5))], self.ip)
            
        # test if Moving_object is instantiated correctly
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        self.assertEqual(mo1.type, int)
        self.assertEqual(mo1.interpolator, self.ip)
        
    def test_len(self):
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        self.assertEqual(len(mo1), 5)
        
    def test_getitem(self):
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        self.assertEqual(mo1[0], self.tpo1)
        self.assertEqual(mo1[1:3], [self.tpo2, self.tpo3])
        
    def test_setitem(self):
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        
        tso_x1 = zeit.TS_Object(12, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 4), dt.datetime(2017, 07, 25, 20, 0, 6)))
        
        # test if TypeError is raised if key is not of type int
        with self.assertRaises(TypeError):
            mo1[0:2] = tso_x1
            
        # test if TypeError is raised if value is not of type sptemp.zeit.TS_Object
        with self.assertRaises(TypeError):
            mo1[1] = 123
            
        # test if ValueError is raised if value.type != Moving_object.type
        with self.assertRaises(ValueError):
            mo1[1] = zeit.TS_Object(12.0, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 4), dt.datetime(2017, 07, 25, 20, 0, 6)))
            
        # test if IndexError is raised if Key is out of range
        with self.assertRaises(IndexError):
            mo1[5] = tso_x1
            
        # test if ValueError is raised if value.ts and other TS_Objects in Moving_Object are not disjoint
        with self.assertRaises(ValueError):
            mo1[-1] = zeit.TS_Object(12, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 22), dt.datetime(2017, 07, 25, 20, 0, 25)))
            
        with self.assertRaises(ValueError):
            mo1[4] = zeit.TS_Object(12, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 22), dt.datetime(2017, 07, 25, 20, 0, 25)))
            
        with self.assertRaises(ValueError):
            mo1[3] = zeit.TS_Object(12, dt.datetime(2017, 07, 25, 20, 0, 4))
            
        with self.assertRaises(ValueError):
            mo1[0] = zeit.TS_Object(12, zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 5)))
            
        with self.assertRaises(ValueError):
            mo1[1] = zeit.TS_Object(12, zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 0, 6), dt.datetime(2017, 07, 25, 20, 0, 11)))
            
        # correct assignment
        mo1[1] = tso_x1
        self.assertEqual(len(mo1), 5)
        self.assertEqual(mo1[1], tso_x1)
        
        mo1[0] = zeit.TS_Object(10, zeit.Time_Period(dt.datetime(2017, 07, 25, 18, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 2)))
        self.assertEqual(mo1[0], zeit.TS_Object(10, zeit.Time_Period(dt.datetime(2017, 07, 25, 18, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 2))))
        
        mo1[4] = zeit.TS_Object(10, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 45)))
        self.assertEqual(mo1[4], zeit.TS_Object(10, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 45))))
        
    def test_delitem(self):
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        mo2 = zeit.Moving_Object([self.tpo1], self.ip)
        
        # test if TypeError is raised if key is not of type int or slice
        with self.assertRaises(TypeError):
            del mo1[20.0]
        
        # test if ValueError is raised if deletion would leave moving_object empty
        with self.assertRaises(ValueError):
            del mo2[0]
            
        with self.assertRaises(ValueError):
            del mo1[:]
            
        # test if correct values are deleted
        del mo1[0:5:3]
        self.assertEqual(len(mo1), 3)
        self.assertEqual(mo1[0], self.tpo2)
        self.assertEqual(mo1[1], self.tpo3)
        self.assertEqual(mo1[2], self.tpo5)
        
        del mo1[0:2]
        self.assertEqual(len(mo1), 1)
        self.assertEqual(mo1[0], self.tpo5)
        
    def test_interpolate(self):
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        
        # test if TypeError is raised if type of time is not datetime.datetime
        with self.assertRaises(TypeError):
            mo1.interpolate(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 45)))
            
        # test if None is returned if time < Moving_Object.start_time() or > Moving_Object.end_time()
        self.assertEqual(mo1.interpolate(dt.datetime(2017, 07, 25, 18, 0, 25)), None)
            
        self.assertEqual(mo1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 45)), None)
        
        # test if correct value is returned
        i_tso1 = mo1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 30))
        self.assertEqual(i_tso1, zeit.TS_Object(20, dt.datetime(2017, 07, 25, 20, 0, 30)))
        
        i_tso2 = mo1.interpolate(dt.datetime(2017, 07, 25, 19, 0, 0))
        self.assertEqual(i_tso2, zeit.TS_Object(10, dt.datetime(2017, 07, 25, 19, 0, 0)))
        
        i_tso3 = mo1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 15))
        self.assertEqual(i_tso3, zeit.TS_Object(15, dt.datetime(2017, 07, 25, 20, 0, 15)))
        
        i_tso4 = mo1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 12))
        self.assertEqual(i_tso4, zeit.TS_Object(15, dt.datetime(2017, 07, 25, 20, 0, 12)))
        
        i_tso5 = mo1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 7))
        self.assertEqual(i_tso5, zeit.TS_Object(12, dt.datetime(2017, 07, 25, 20, 0, 7)))
        
        i_tso6 = mo1.interpolate(dt.datetime(2017, 07, 25, 20, 0, 27))
        self.assertEqual(i_tso6, zeit.TS_Object(19, dt.datetime(2017, 07, 25, 20, 0, 27)))
        
    def test_slice(self):
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        
        # test if TypeError is raised if time is not of type sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            mo1.slice(dt.datetime(2017, 07, 25, 20, 0, 25), self.ip)
            
        # test if None is returned if slice is empty
        self.assertEqual(mo1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 18, 0, 25), dt.datetime(2017, 07, 25, 18, 0, 45))), None)
            
        self.assertEqual(mo1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 35), dt.datetime(2017, 07, 25, 20, 0, 45))), None)
            
        self.assertEqual(mo1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 2), dt.datetime(2017, 07, 25, 20, 0, 4))), None)
            
        # test if correct slice is returned
        s1 = mo1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 18, 0, 2), dt.datetime(2017, 07, 25, 19, 30, 0)))
        self.assertEqual(len(s1), 1)
        self.assertEqual(s1[0], zeit.TS_Object(10, zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 0, 0), dt.datetime(2017, 07, 25, 19, 30, 0))))
        
        s2 = mo1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 30), dt.datetime(2017, 07, 25, 20, 0, 45)))
        self.assertEqual(len(s2), 1)
        self.assertEqual(s2[0], zeit.TS_Object(20, dt.datetime(2017, 07, 25, 20, 0, 30)))
        
        s3 = mo1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 2), dt.datetime(2017, 07, 25, 20, 0, 7)))
        self.assertEqual(len(s3), 1)
        self.assertEqual(s3[0], zeit.TS_Object(12, dt.datetime(2017, 07, 25, 20, 0, 5)))
        
        s4 = mo1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 15), dt.datetime(2017, 07, 25, 20, 0, 19)))
        self.assertEqual(len(s4), 2)
        self.assertEqual(s4[0], zeit.TS_Object(15, dt.datetime(2017, 07, 25, 20, 0, 15)))
        self.assertEqual(s4[1], zeit.TS_Object(18, dt.datetime(2017, 07, 25, 20, 0, 19)))
        
        s5 = mo1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 12), dt.datetime(2017, 07, 25, 20, 0, 20)))
        self.assertEqual(len(s5), 2)
        self.assertEqual(s5[0], zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 12), dt.datetime(2017, 07, 25, 20, 0, 15))))
        self.assertEqual(s5[1], zeit.TS_Object(18, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 19), dt.datetime(2017, 07, 25, 20, 0, 20))))
        
        s6 = mo1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.assertEqual(len(s6), 5)
        self.assertEqual(s6[0], zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 0)))
        self.assertEqual(s6[-1], zeit.TS_Object(20, dt.datetime(2017, 07, 25, 20, 0, 30)))
        
        s7 = mo1.slice(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 4), dt.datetime(2017, 07, 25, 20, 0, 22)))
        self.assertEqual(len(s7), 3)
        self.assertEqual(s7[0], zeit.TS_Object(12, dt.datetime(2017, 07, 25, 20, 0, 5)))
        self.assertEqual(s7[-1], zeit.TS_Object(18, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 19), dt.datetime(2017, 07, 25, 20, 0, 22))))
        
    def test_resampled_slice(self):
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        
        # test if TypeError is raised if times is not of type list
        with self.assertRaises(TypeError):
            mo1.resampled_slice(dt.datetime(2017, 07, 25, 20, 0, 0))
            
        # test if TypeError is raised if interpolator not of type sptemp.zeit.Interpolator
        with self.assertRaises(TypeError):
            mo1.resampled_slice(dt.datetime(2017, 07, 25, 20, 0, 0), 123)
            
        # test if ValueError is raised if length times < 2
        with self.assertRaises(ValueError):
            mo1.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 0)])
            
        rs1 = mo1.resampled_slice([dt.datetime(2017, 07, 25, 18, 0, 0), dt.datetime(2017, 07, 25, 18, 20, 0)])
        rs2 = mo1.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 40), dt.datetime(2017, 07, 25, 20, 0, 50)])
        rs3 = mo1.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 30), dt.datetime(2017, 07, 25, 20, 0, 50)])
        rs4 = mo1.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 12), dt.datetime(2017, 07, 25, 20, 0, 17), dt.datetime(2017, 07, 25, 20, 0, 25)])
        rs5 = mo1.resampled_slice([dt.datetime(2017, 07, 25, 20, 0, 24), dt.datetime(2017, 07, 25, 20, 0, 26), dt.datetime(2017, 07, 25, 20, 0, 28)])
        
        self.assertEqual(rs1, None)
        self.assertEqual(rs2, None)
        self.assertEqual(len(rs3), 1)
        self.assertEqual(rs3[0], zeit.TS_Object(20, dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.assertEqual(len(rs4), 4)
        self.assertEqual(rs4.as_list(), [zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 12), dt.datetime(2017, 07, 25, 20, 0, 15))),
                                         zeit.TS_Object(15, dt.datetime(2017, 07, 25, 20, 0, 17)),
                                         zeit.TS_Object(18, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 19), dt.datetime(2017, 07, 25, 20, 0, 22))),
                                         zeit.TS_Object(18, dt.datetime(2017, 07, 25, 20, 0, 25))])
        self.assertEqual(len(rs5), 3)
        self.assertEqual(rs5.as_list(), [zeit.TS_Object(18, dt.datetime(2017, 07, 25, 20, 0, 24)),
                                         zeit.TS_Object(19, dt.datetime(2017, 07, 25, 20, 0, 26)),
                                         zeit.TS_Object(19, dt.datetime(2017, 07, 25, 20, 0, 28))])
        
    def test_as_list(self):
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3], self.ip)
        self.assertEqual(mo1.as_list(), [self.tpo1, self.tpo2, self.tpo3])
        
    def test_i_object(self):
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        self.assertEqual(mo1.i_object(0), self.tpo1)
        
    def test_prev_ti(self):
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        
        # test if TypeError is raised if time not of type datetime.datetime
        with self.assertRaises(TypeError):
            mo1.prev_i(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 45)))
            
        # test if correct values are returned
        self.assertEqual(mo1.prev_i(dt.datetime(2017, 07, 25, 18, 0, 31)), None)
        self.assertEqual(mo1[mo1.prev_i(dt.datetime(2017, 07, 25, 20, 0, 31))], self.tpo5)
        self.assertEqual(mo1[mo1.prev_i(dt.datetime(2017, 07, 25, 20, 0, 5))], self.tpo2)
        self.assertEqual(mo1[mo1.prev_i(dt.datetime(2017, 07, 25, 20, 0, 12))], self.tpo3)
        self.assertEqual(mo1[mo1.prev_i(dt.datetime(2017, 07, 25, 20, 0, 19))], self.tpo4)
        self.assertEqual(mo1[mo1.prev_i(dt.datetime(2017, 07, 25, 20, 0, 24))], self.tpo4)
        
    def test_next_ts(self):
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        
        # test if TypeError is raised if time not of type datetime.datetime
        with self.assertRaises(TypeError):
            mo1.next_i(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 45)))
            
        # test if correct values are returned
        self.assertEqual(mo1.next_i(dt.datetime(2017, 07, 25, 20, 0, 31)), None)
        self.assertEqual(mo1[mo1.next_i(dt.datetime(2017, 07, 25, 18, 0, 31))], self.tpo1)
        self.assertEqual(mo1[mo1.next_i(dt.datetime(2017, 07, 25, 20, 0, 0))], self.tpo1)
        self.assertEqual(mo1[mo1.next_i(dt.datetime(2017, 07, 25, 20, 0, 5))], self.tpo2)
        self.assertEqual(mo1[mo1.next_i(dt.datetime(2017, 07, 25, 20, 0, 12))], self.tpo3)
        self.assertEqual(mo1[mo1.next_i(dt.datetime(2017, 07, 25, 20, 0, 17))], self.tpo4)
        self.assertEqual(mo1[mo1.next_i(dt.datetime(2017, 07, 25, 20, 0, 22))], self.tpo4)
        self.assertEqual(mo1[mo1.next_i(dt.datetime(2017, 07, 25, 20, 0, 26))], self.tpo5)
        self.assertEqual(mo1[mo1.next_i(dt.datetime(2017, 07, 25, 20, 0, 30))], self.tpo5)
        
    def test_start_time(self):
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3], self.ip)
        self.assertEqual(mo1.start_time(), self.tpo1.start_time())
        
    def test_end_time(self):
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3], self.ip)
        self.assertEqual(mo1.end_time(), self.tpo3.end_time())
        
    def test_append(self):
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        
        # test if TypeError is raised if value is not of type sptemp.zeit.TS_Object
        with self.assertRaises(TypeError):
            mo1.append(123)
           
        # test if ValueError is raised if TS_Object.start_time() <= Moving_Object.end_time()
        with self.assertRaises(ValueError):
            mo1.append(zeit.TS_Object(10, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 30), dt.datetime(2017, 07, 25, 20, 0, 32))))
            
        with self.assertRaises(ValueError):
            mo1.append(zeit.TS_Object(10, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 23), dt.datetime(2017, 07, 25, 20, 0, 32))))
        
        with self.assertRaises(ValueError):
            mo1.append(zeit.TS_Object(10, dt.datetime(2017, 07, 25, 20, 0, 30)))
            
        # test if correct value is appended
        mo1.append(zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 40), dt.datetime(2017, 07, 25, 20, 0, 45))))
        self.assertEqual(len(mo1), 6)
        self.assertEqual(mo1[-1], zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 40), dt.datetime(2017, 07, 25, 20, 0, 45))))
        
    def test_insert(self):
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        
        # test if TypeError is raised if value is not of type sptemp.zeit.TS_Object
        with self.assertRaises(TypeError):
            mo1.insert(123)
            
        # test if ValueError is raised if value.type != Moving_Objec.type
        with self.assertRaises(ValueError):
            mo1.insert(zeit.TS_Object(15.0, dt.datetime(2017, 07, 25, 19, 0, 45)))
            
        # test if ValueError is raised if value.ts and existing timestamps in Moving_Object
        with self.assertRaises(ValueError):
            mo1.insert(zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 18, 0, 40), dt.datetime(2017, 07, 25, 19, 0, 45))))
            
        with self.assertRaises(ValueError):
            mo1.insert(zeit.TS_Object(15, dt.datetime(2017, 07, 25, 19, 0, 45)))
            
        with self.assertRaises(ValueError):
            mo1.insert(zeit.TS_Object(15, dt.datetime(2017, 07, 25, 20, 0, 0)))
            
        with self.assertRaises(ValueError):
            mo1.insert(zeit.TS_Object(15, dt.datetime(2017, 07, 25, 20, 0, 5)))
            
        with self.assertRaises(ValueError):
            mo1.insert(zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 4))))
            
        with self.assertRaises(ValueError):
            mo1.insert(zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 1), dt.datetime(2017, 07, 25, 20, 0, 10))))
            
        with self.assertRaises(ValueError):
            mo1.insert(zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 12), dt.datetime(2017, 07, 25, 20, 0, 16))))
            
        with self.assertRaises(ValueError):
            mo1.insert(zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 16), dt.datetime(2017, 07, 25, 20, 0, 19))))
            
        with self.assertRaises(ValueError):
            mo1.insert(zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 30), dt.datetime(2017, 07, 25, 20, 0, 45))))
        
        with self.assertRaises(ValueError):
            mo1.insert(zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 18, 0, 30), dt.datetime(2017, 07, 25, 20, 0, 45))))
            
        # test if correct value is inserted
        mo1.insert(zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 18, 0, 30), dt.datetime(2017, 07, 25, 18, 0, 45))))
        self.assertEqual(len(mo1), 6)
        self.assertEqual(mo1[0], zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 18, 0, 30), dt.datetime(2017, 07, 25, 18, 0, 45))))
        
        mo1.insert(zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 35), dt.datetime(2017, 07, 25, 20, 0, 45))))
        self.assertEqual(len(mo1), 7)
        self.assertEqual(mo1[-1], zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 35), dt.datetime(2017, 07, 25, 20, 0, 45))))
        
        mo1.insert(zeit.TS_Object(12, dt.datetime(2017, 07, 25, 20, 0, 3)))
        self.assertEqual(len(mo1), 8)
        self.assertEqual(mo1[2], zeit.TS_Object(12, dt.datetime(2017, 07, 25, 20, 0, 3)))
        
        mo1.insert(zeit.TS_Object(22, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 27))))
        self.assertEqual(len(mo1), 9)
        self.assertEqual(mo1[6], zeit.TS_Object(22, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 27))))
        
    def test_delete(self):
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        
        # test if TypeError is raised if type of time is not sptemp.zeit.Time_Period
        with self.assertRaises(TypeError):
            mo1.delete(dt.datetime(2017, 07, 25, 20, 0, 5))
            
        # test if ValueError is raised if deletion would leave Moving Object empty
        with self.assertRaises(ValueError):
            mo1.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 18, 0, 25), dt.datetime(2017, 07, 25, 20, 0, 45)))
            
        # check if values are deleted correctly
        mo1.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 18, 0, 25), dt.datetime(2017, 07, 25, 18, 0, 45)))
        self.assertEqual(len(mo1), 5)
        self.assertEqual(mo1[0], self.tpo1)
        
        mo1.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 31), dt.datetime(2017, 07, 25, 20, 0, 45)))
        self.assertEqual(len(mo1), 5)
        self.assertEqual(mo1[4], self.tpo5)
        
        mo1.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 10), dt.datetime(2017, 07, 25, 20, 0, 14)))
        self.assertEqual(len(mo1), 6)
        self.assertEqual(mo1[2], zeit.TS_Object(15, dt.datetime(2017, 07, 25, 20, 0, 10)))
        self.assertEqual(mo1[3], zeit.TS_Object(15, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 14), dt.datetime(2017, 07, 25, 20, 0, 15))))
        
        mo1.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 20), dt.datetime(2017, 07, 25, 20, 0, 22)))
        self.assertEqual(len(mo1), 7)
        self.assertEqual(mo1[4], zeit.TS_Object(18, zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 19), dt.datetime(2017, 07, 25, 20, 0, 20))))
        self.assertEqual(mo1[5], zeit.TS_Object(18, dt.datetime(2017, 07, 25, 20, 0, 22)))
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        mo1.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 18, 0, 20), dt.datetime(2017, 07, 25, 19, 50, 30)))
        self.assertEqual(len(mo1), 5)
        self.assertEqual(mo1[0], zeit.TS_Object(10, zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 50, 30), dt.datetime(2017, 07, 25, 20, 0, 0))))
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        mo1.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 18, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 5)))
        self.assertEqual(len(mo1), 4)
        self.assertEqual(mo1[0], zeit.TS_Object(12, dt.datetime(2017, 07, 25, 20, 0, 5)))
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        mo1.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 30, 0), dt.datetime(2017, 07, 25, 20, 0, 22)))
        self.assertEqual(len(mo1), 3)
        self.assertEqual(mo1[1], zeit.TS_Object(18, dt.datetime(2017, 07, 25, 20, 0, 22)))
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        mo1.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 5), dt.datetime(2017, 07, 25, 20, 0, 45)))
        self.assertEqual(len(mo1), 2)
        self.assertEqual(mo1[1], zeit.TS_Object(12, dt.datetime(2017, 07, 25, 20, 0, 5)))
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        mo1.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 19), dt.datetime(2017, 07, 25, 20, 0, 30)))
        self.assertEqual(len(mo1), 5)
        self.assertEqual(mo1[3], zeit.TS_Object(18, dt.datetime(2017, 07, 25, 20, 0, 19)))
        self.assertEqual(mo1[4], zeit.TS_Object(20, dt.datetime(2017, 07, 25, 20, 0, 30)))
        
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        mo1.delete(zeit.Time_Period(dt.datetime(2017, 07, 25, 20, 0, 1), dt.datetime(2017, 07, 25, 20, 0, 4)))
        self.assertEqual(len(mo1), 5)
        self.assertEqual(mo1[0], zeit.TS_Object(10, zeit.Time_Period(dt.datetime(2017, 07, 25, 19, 0, 0), dt.datetime(2017, 07, 25, 20, 0, 0))))
        self.assertEqual(mo1[1], zeit.TS_Object(12, dt.datetime(2017, 07, 25, 20, 0, 5)))
        
    def test_length(self):
        mo1 = zeit.Moving_Object([self.tpo1, self.tpo2, self.tpo3, self.tpo4, self.tpo5], self.ip)
        self.assertEqual(mo1.length(), 5)
    
        
unittest.main()
        
        