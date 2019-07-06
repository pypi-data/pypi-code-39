# -*- coding: utf-8 -*-
"""
This module contains the following interpolation functions:

    ICollection:
        undefined()
        prev_ts()
        next_ts()
        linear()
        
    IPoint:
        linear_point()
        curve_point()
        
    ICurve:
        basic_linear()
        
    IRing:
        linear_translation()
        basic_linear()

Todo:
 
"""

import datetime as dt
import copy
import math
import bisect

import shapely.geometry as sg
import shapely.affinity as sa

from sptemp import zeit
from sptemp import moving_geometry as mg
from sptemp import _texts as text


class ICollection:
    """This class provides a collection of general interpolation functionality
    """
    
    @staticmethod
    def undefined(start_ts, end_ts, time, *args):
        """
        Args:
            start_ts (sptemp.zeit.TS_Object or NoneType): previous TS_Object
            end_ts (sptemp.zeit.TS_Object): next TS_Object
            time (datetime.datetime): time for which value will be interpolated
            *args: Arbitrary arguments
            
        Returns:
            NoneType: Function always returns None
        """
        return None
        
    @staticmethod
    def constant(start_ts, end_ts, time, *args):
        """Constant Movement where value of start_ts is returned
        
        Args:
            start_ts (sptemp.zeit.TS_Object): previous TS_Object
            end_ts (sptemp.zeit.TS_Object): next TS_Object
            time (datetime.datetime): time for which value will be interpolated
            *args: Arbitrary arguments (included for compatibility reasons)
            
        Returns:
            TS_Object or NoneType: a TS_Object is returned |br|
            TS_Object.ts = time |br|
            if time < end_ts.start_time(): TS_Object.value = start_ts |br|
            else: TS_Object.value = end_ts
        """
        if time < end_ts.start_time():
            return start_ts.__class__(start_ts.value, time) if hasattr(start_ts, "crs") is False else start_ts.__class__(start_ts.value, time, start_ts.crs)
        
        else:
            return end_ts.__class__(end_ts.value, time) if hasattr(end_ts, "crs") is False else end_ts.__class__(end_ts.value, time, end_ts.crs)
        
    @staticmethod
    def next_ts(start_ts, end_ts, time, *args):
        """Constant Movement where value of end_ts is returned
        
        Args:
            start_ts (sptemp.zeit.TS_Object): previous TS_Object of time
            end_ts (sptemp.zeit.TS_Object): next TS_Object of time
            time (datetime.datetime): time for which value will be interpolated
            *args: Arbitrary arguments (included for compatibility reasons)
            
        Returns:
            TS_Object: a TS_Object is returned |br|
            TS_Object.ts = time |br|
            if time > start_ts.end_time(): TS_Object.value = end_ts |br|
            else: TS_Object.value = start_ts
        """
        if time > start_ts.end_time():
            return end_ts.__class__(end_ts.value, time) if hasattr(end_ts, "crs") is False else end_ts.__class__(end_ts.value, time, end_ts.crs)
        
        else:
            return start_ts.__class__(start_ts.value, time) if hasattr(start_ts, "crs") is False else start_ts.__class__(start_ts.value, time, start_ts.crs)
    
    @staticmethod
    def linear(start_ts, end_ts, time, *args):
        """Linear interpolation-function for numeric values
        
        Note:
            Value of TS_Objects should be of numeric type!
        
        Args:
            start_ts (sptemp.zeit.TS_Object): previous TS_Object of time
            end_ts (sptemp.zeit.TS_Object): next TS_Object of time
            time (datetime.datetime): time for which value will be interpolated
            *args: Arbitrary arguments (included for compatibility reasons)
            
        Returns:
            TS_Object: a TS_Object is returned |br|
            TS_Object.ts = time |br|
            TS_Object.value: interpolated value at 'time' |br|
            
        Raises:
            ValueError: if start_ts.type != end_ts.type OR start_ts.end_time() >= end_ts.start_time().
            TypeError: if type(time) != datetime.datetime
        """
        if isinstance(start_ts, zeit.TS_Object) is False or isinstance(end_ts, zeit.TS_Object) is False:
            raise TypeError(text.IC_Texts.error1)
        
        elif isinstance(time, dt.datetime) is False:
            raise TypeError(text.IC_Texts.error2)
        
        if start_ts.type != end_ts.type:
            raise ValueError(text.IC_Texts.error3)
        
        elif start_ts.end_time() >= end_ts.start_time():
            raise ValueError(text.IC_Texts.error4)
        
        else:
            tdelta_total = end_ts.start_time() - start_ts.end_time()
            tdelta_time = time - start_ts.end_time()
            t_ratio = tdelta_time.total_seconds()/float(tdelta_total.total_seconds())
            vdelta_total = end_ts.value - start_ts.value
            vdelta_time = vdelta_total*t_ratio + start_ts.value
            
            if isinstance(start_ts.value, int):
                return zeit.TS_Object(int(vdelta_time), time)
            else:
                return zeit.TS_Object(vdelta_time, time)
            

class IPoint:
    """This class provides interpolation functionality for TS_Point objects.
    
    Note:
        The interpolation functionality provided by this class is only suited for cartesian coordinates.
    """
    
    @staticmethod
    def linear_point(start_ts, end_ts, time, *args):
        """Linear Interpolation between TS_Point objects
        
        Args:
            start_ts (sptemp.moving_geometry.TS_Point): previous TS_Point of time
            end_ts (sptemp.moving_geometry.TS_Point): next TS_Point of time
            time (datetime.datetime): time for which value will be interpolated
            *args: Arbitrary arguments (included for compatibility reasons)
            
        Returns:
            sptemp.moving_geometry.TS_Point: TS_Point with ts = time
        
        Raises:
            TypeError: if start_ts or end_ts is not of type sptemp.moving_geometry.TS_Point
                OR time is not of type datetime.datetime
            ValueError: If start_ts.has_z != end_ts.has_z OR if start_ts.end_time() > end_ts.start_time()
                OR if time < start_ts.end_time() OR if time > end_ts.start_time()
        """
        if isinstance(start_ts, mg.TS_Point) is False or isinstance(end_ts, mg.TS_Point) is False:
            raise TypeError(text.IPoint_Texts.lp_error1)
        
        elif isinstance(time, dt.datetime) is False:
            raise TypeError(text.IPoint_Texts.lp_error2)
        
        elif start_ts.has_z != end_ts.has_z:
            raise ValueError(text.IPoint_Texts.lp_error3)
        
        elif start_ts.end_time() >= end_ts.start_time():
            raise ValueError(text.IPoint_Texts.lp_error4)
        
        elif time < start_ts.end_time() or time > end_ts.start_time():
            raise ValueError(text.IPoint_Texts.lp_error5)
        
        elif start_ts.crs is None and end_ts.crs is not None or start_ts.crs is not None and end_ts.crs is None:
            raise ValueError(text.IPoint_Texts.lp_error6)
        
        elif start_ts.crs is not None and start_ts.crs.srs != end_ts.crs.srs:
            raise ValueError(text.IPoint_Texts.lp_error6)
        
        t = (time - start_ts.end_time()).total_seconds()/(end_ts.start_time() - start_ts.end_time()).total_seconds()
        
        if start_ts.has_z:
            val =  sg.Point(I_Helper.linear_point((start_ts.value.x, start_ts.value.y, start_ts.value.z),
                                                  (end_ts.value.x, end_ts.value.y, end_ts.value.z), t))
        else:
            val =  sg.Point(I_Helper.linear_point((start_ts.value.x, start_ts.value.y),
                                                  (end_ts.value.x, end_ts.value.y), t))
            
        return mg.TS_Point(val, time, start_ts.crs)
            
    @staticmethod
    def curve_point(start_ts, end_ts, time, curve):
        """Linear Interpolation between TS_Point objects, where the point follows the course defined by a LineString.
        
        Args:
            start_ts (sptemp.moving_geometry.TS_Point): previous TS_Point of time
            end_ts (sptemp.moving_geometry.TS_Point): next TS_Point of time
            time (datetime.datetime): time for which value will be interpolated
            curve (shapely.geometry.LineString): LineString the point moves along
            
        Returns:
            sptemp.moving_geometry.TS_Point: TS_Point with ts = time
        
        Raises:
            TypeError: if start_ts or end_ts is not of type sptemp.moving_object.TS_Point
                OR time is not of type datetime.datetime OR curve is not of type shapely.geometry.LineString
            ValueError: If start_ts.end_time > end_ts.start_time() OR
                start_ts.has_z, end_ts.has_z and curve.has_z are not equal OR start_ts.crs != end_ts.crs OR
                time < start_ts.end_time() OR time > end_ts.start_time() OR start_ts.value is not equal
                to start point of curve OR end_ts.value is not equal to end point of curve
        """
        if isinstance(start_ts, mg.TS_Point) is False or isinstance(end_ts, mg.TS_Point) is False:
            raise TypeError(text.IPoint_Texts.c_error1)
        
        elif isinstance(time, dt.datetime) is False:
            raise TypeError(text.IPoint_Texts.c_error2)
        
        elif isinstance(curve, sg.LineString) is False:
            raise TypeError(text.IPoint_Texts.c_error3)
        
        elif start_ts.has_z != end_ts.has_z or start_ts.has_z != curve.has_z:
            raise ValueError(text.IPoint_Texts.c_error4)
        
        elif start_ts.crs is None and end_ts.crs is not None or start_ts.crs is not None and end_ts.crs is None:
            raise ValueError(text.IPoint_Texts.c_error5)
        
        elif start_ts.crs is not None and start_ts.crs.srs != end_ts.crs.srs:
            raise ValueError(text.IPoint_Texts.c_error5)
        
        elif start_ts.end_time() >= end_ts.start_time():
            raise ValueError(text.IPoint_Texts.c_error6)
        
        elif time < start_ts.end_time() or time > end_ts.start_time():
            raise ValueError(text.IPoint_Texts.c_error7)
        
        elif start_ts.value != sg.Point(curve.coords[0]) or end_ts.value != sg.Point(curve.coords[-1]):
            raise ValueError(text.IPoint_Texts.c_error8)
        
        t = (time - start_ts.end_time()).total_seconds()/(end_ts.start_time() - start_ts.end_time()).total_seconds()
        
        if start_ts.has_z:
            len_t = 0
            start_p = None
            end_p = None
            len_seg = None
            
            for i in range(len(curve.coords) - 1):
                
                len_t += I_Helper.z_dictance(curve.coords[i], curve.coords[i+1])
            
            len_t = t*len_t
            
            for i in range(len(curve.coords) - 1):
                
                len_seg = I_Helper.z_dictance(curve.coords[i], curve.coords[i+1])
                
                if len_t - len_seg <= 0:
                    start_p = curve.coords[i]
                    end_p = curve.coords[i+1]
                    break
                else:
                    len_t -= len_seg
            
            seg_t = len_t/len_seg
            x = (1 - seg_t)*start_p[0] + seg_t*end_p[0]
            y = (1 - seg_t)*start_p[1] + seg_t*end_p[1]
            z = (1 - seg_t)*start_p[2] + seg_t*end_p[2]
            
            return mg.TS_Point(sg.Point(round(x,8), round(y,8), round(z,8)), time, start_ts.crs)   
        
        else:
            len_t = t*curve.length
            start_p = None
            end_p = None
            len_seg = None
            
            for i in range(len(curve.coords) - 1):
                
                len_seg = sg.LineString([curve.coords[i], curve.coords[i+1]]).length
                
                if len_t - len_seg <= 0:
                    start_p = curve.coords[i]
                    end_p = curve.coords[i+1]
                    break
                else:
                    len_t -= len_seg
                    
            seg_t = len_t/len_seg
            x = (1 - seg_t)*start_p[0] + seg_t*end_p[0]
            y = (1 - seg_t)*start_p[1] + seg_t*end_p[1]
            
            return mg.TS_Point(sg.Point(round(x,8), round(y,8)), time, start_ts.crs)
        
        
class ICurve:
    """This class provides interpolation functionality for TS_LineString objects.
    
    Note:
        The interpolation functionality provided by this class is only suited for cartesian coordinates.
    """
    
    @staticmethod
    def basic_linear(start_ts, end_ts, time, s_type="angle"):
        """Linear Interpolation between two LineStrings.
        
        Note:
            only x- and y-coordinate values are taken into account for linestring simplification
        
        Args:
            start_ts (sptemp.moving_geometry.TS_LineString): previous TS_LineString of time
            end_ts (sptemp.moving_geometry.TS_LineString): next TS_LineString of time
            time (datetime.datetime): time for which value will be interpolated
            s_type (string): defines line simplification type: 'angle' or 'distance'
            
        Returns:
            sptemp.moving_geometry.TS_LineString: returns TS_Linestring with ts = time
        
        Raises:
            TypeError: if start_ts or end_ts is not of type sptemp.moving_object.TS_LineString
                OR time is not of type datetime.datetime
            ValueError: If start_ts.has_z != end_ts.has_z OR if start_ts.end_time > end_ts.start_time()
                OR start_ts.crs != end_ts.crs OR time < start_ts.end_time() OR time > end_ts.start_time()
        """
        if isinstance(start_ts, mg.TS_LineString) is False or isinstance(end_ts, mg.TS_LineString) is False:
            raise TypeError(text.ICurve_Texts.bl_error1)
        
        elif isinstance(time, dt.datetime) is False:
            raise TypeError(text.ICurve_Texts.bl_error2)
        
        elif start_ts.has_z != end_ts.has_z:
            raise ValueError(text.ICurve_Texts.bl_error3)
        
        elif start_ts.crs is None and end_ts.crs is not None or start_ts.crs is not None and end_ts.crs is None:
            raise ValueError(text.ICurve_Texts.bl_error4)
        
        elif start_ts.crs is not None and start_ts.crs.srs != end_ts.crs.srs:
            raise ValueError(text.ICurve_Texts.bl_error4)
        
        elif start_ts.end_time() >= end_ts.start_time():
            raise ValueError(text.ICurve_Texts.bl_error5)
        
        elif time < start_ts.end_time() or time > end_ts.start_time():
            raise ValueError(text.ICurve_Texts.bl_error6)
        
        elif s_type not in ["angle", "distance"]:
            raise ValueError(text.ICurve_Texts.bl_error7)
        
        if time == start_ts.end_time():
            return mg.TS_LineString(start_ts.value, time, start_ts.crs)
        elif time == end_ts.start_time():
            return mg.TS_LineString(end_ts.value, time, end_ts.crs)
        
        line_t = (time - start_ts.end_time()).total_seconds()/(end_ts.start_time() - start_ts.end_time()).total_seconds()
        
        if s_type == "angle":
            val = I_Helper.linear_curve(start_ts.value, end_ts.value, line_t, "angle")
        else:
            val = I_Helper.linear_curve(start_ts.value, end_ts.value, line_t, "distance")
        
        return mg.TS_LineString(val, time, start_ts.crs)

        
class IRing:
    """This class provides interpolation functionality for TS_LinearRing objects.
    
    Note:
        The interpolation functionality provided by this class is only suited for cartesian coordinates.
    """
    
    @staticmethod
    def linear_translation(start_ts, end_ts, time):
        """Linear translation of start_ts.value towards end_ts.value.centroid.
        Shape of LinearRings of start_ts and end_ts should be equal. 
        
        Note:
            translation only based on x and y-coordinates
        
        Args:
            start_ts (sptemp.moving_geometry.TS_LinearRing): previous TS_LinearRing of time
            end_ts (sptemp.moving_geometry.TS_LinearRing): next TS_LinearRing of time
            time (datetime.datetime): time for which value will be interpolated
            
        Returns:
            sptemp.moving_geometry.TS_LinearRing: TS_LinearRing with ts = time
        
        Raises:
            TypeError: if start_ts or end_ts is not of type sptemp.moving_object.TS_LinearRing
                OR time is not of type datetime.datetime
            ValueError: If start_ts.has_z != end_ts.has_z OR if start_ts.end_time > end_ts.start_time()
                OR start_ts.crs != end_ts.crs OR time < start_ts.end_time() OR time > end_ts.start_time()
        """
        if isinstance(start_ts, mg.TS_LinearRing) is False or isinstance(end_ts, mg.TS_LinearRing) is False:
            raise TypeError(text.IRing_Texts.lt_error1)
        
        elif isinstance(time, dt.datetime) is False:
            raise TypeError(text.IRing_Texts.lt_error2)
        
        elif start_ts.has_z != end_ts.has_z:
            raise ValueError(text.IRing_Texts.lt_error3)
        
        elif start_ts.crs is None and end_ts.crs is not None or start_ts.crs is not None and end_ts.crs is None:
            raise ValueError(text.IRing_Texts.lt_error4)
        
        elif start_ts.crs is not None and start_ts.crs.srs != end_ts.crs.srs:
            raise ValueError(text.IRing_Texts.lt_error4)
        
        elif start_ts.end_time() >= end_ts.start_time():
            raise ValueError(text.IRing_Texts.lt_error5)
        
        elif time < start_ts.end_time() or time > end_ts.start_time():
            raise ValueError(text.IRing_Texts.lt_error6)
        
        if time == start_ts.end_time():
            return start_ts.value
        elif time == end_ts.start_time():
            return end_ts.value
        
        t = (time - start_ts.end_time()).total_seconds()/(end_ts.start_time() - start_ts.end_time()).total_seconds()
        
        start_c = start_ts.value.centroid
        end_c = end_ts.value.centroid
        
        x_off = end_c.x - start_c.x
        y_off = end_c.y - start_c.y
        
        return mg.TS_LinearRing(sg.LinearRing(sa.translate(start_ts.value, t*x_off, t*y_off).coords[:]), time, start_ts.crs)
    
    @staticmethod
    def basic_linear(start_ts, end_ts, time, s_type="angle"):
        """Linear Interpolation of LinearRings.
        
        Note:
            matching of control points only based on x and y-coordinates
        
        Args:
            start_ts (sptemp.moving_geometry.TS_LinearRing): previous TS_LinearRing of time
            end_ts (sptemp.moving_geometry.TS_LinearRing): next TS_LinearRing of time
            time (datetime.datetime): time for which value will be interpolated
            s_type (string): defines line simplification type: 'angle' or 'distance'
            
        Returns:
            sptemp.moving_geometry.TS_LinearRing: TS_LinearRing with ts = time
        
        Raises:
            TypeError: if start_ts or end_ts is not of type sptemp.moving_object.TS_LinearRing
                OR time is not of type datetime.datetime
            ValueError: If start_ts.has_z != end_ts.has_z OR if start_ts.end_time > end_ts.start_time()
                OR start_ts.crs != end_ts.crs OR time < start_ts.end_time() OR time > end_ts.start_time()
        """
        if isinstance(start_ts, mg.TS_LinearRing) is False or isinstance(end_ts, mg.TS_LinearRing) is False:
            raise TypeError(text.IRing_Texts.lt_error1)
        
        elif isinstance(time, dt.datetime) is False:
            raise TypeError(text.IRing_Texts.lt_error2)
        
        elif start_ts.has_z != end_ts.has_z:
            raise ValueError(text.IRing_Texts.lt_error3)
        
        elif start_ts.crs is None and end_ts.crs is not None or start_ts.crs is not None and end_ts.crs is None:
            raise ValueError(text.IRing_Texts.lt_error4)
        
        elif start_ts.crs is not None and start_ts.crs.srs != end_ts.crs.srs:
            raise ValueError(text.IRing_Texts.lt_error4)
        
        elif start_ts.end_time() >= end_ts.start_time():
            raise ValueError(text.IRing_Texts.lt_error5)
        
        elif time < start_ts.end_time() or time > end_ts.start_time():
            raise ValueError(text.IRing_Texts.lt_error6)
        
        elif s_type not in ["angle", "distance"]:
            raise ValueError(text.IRing_Texts.lt_error7)
        
        if time == start_ts.end_time():
            return start_ts.value
        elif time == end_ts.start_time():
            return end_ts.value
        
        tx = (time - start_ts.end_time()).total_seconds()/(end_ts.start_time() - start_ts.end_time()).total_seconds()
        
        curve1 = start_ts.value if start_ts.value.is_ccw else sg.LinearRing(start_ts.value.coords[::-1])
        curve2 = end_ts.value if end_ts.value.is_ccw else sg.LinearRing(end_ts.value.coords[::-1])
        
        curve1_convex = curve1.convex_hull.exterior if curve1.convex_hull.exterior.is_ccw else sg.LinearRing(curve1.convex_hull.exterior.coords[::-1])
        curve2_convex = curve2.convex_hull.exterior if curve2.convex_hull.exterior.is_ccw else sg.LinearRing(curve2.convex_hull.exterior.coords[::-1])
        
        curve1_seg = I_Helper.curve_segments(curve1)
        curve1_convex_seg = I_Helper.curve_segments(curve1_convex)
        curve2_seg = I_Helper.curve_segments(curve2)
        curve2_convex_seg = I_Helper.curve_segments(curve2_convex)
        
        curve1_diff = I_Helper.create_diff_dict(curve1_convex_seg, curve1_seg)
        curve2_diff = I_Helper.create_diff_dict(curve2_convex_seg, curve2_seg)
        
        # angle list: [(angle, start_index, end_index), (...)]
        ang_curve1 = [I_Helper.angle_to_x_axis(seg[0], seg[-1]) for seg in curve1_convex_seg]
        ang_curve1.sort()
        ang_curve2 = [I_Helper.angle_to_x_axis(seg[0], seg[-1]) for seg in curve2_convex_seg]
        ang_curve2.sort()
        
        # find starting segments -> smallest difference in angels
        st1 = 0
        st2 = 0
        ang = 360
        for i,seg1 in enumerate(ang_curve1):
            for x,seg2 in enumerate(ang_curve2):
                if abs(seg1 - seg2) < ang:
                    st1 = i
                    st2 = x
                    ang = abs(seg1 - seg2)
                    
        curve1_seg = [seg if i not in curve1_diff else curve1_diff[i] for i,seg in enumerate(curve1_convex_seg)]
        curve2_seg = [seg if i not in curve2_diff else curve2_diff[i] for i,seg in enumerate(curve2_convex_seg)]
        
        curve1_seg_final = curve1_seg[st1:]
        for seg in curve1_seg[:st1]:
            curve1_seg_final.append(seg)
            
        curve2_seg_final = curve2_seg[st2:]
        for seg in curve2_seg[:st2]:
            curve2_seg_final.append(seg)

        curve1 = I_Helper.linestring_from_segments(curve1_seg_final)
        curve2 = I_Helper.linestring_from_segments(curve2_seg_final)
        
        if s_type == "angle":
            val = sg.LinearRing(I_Helper.linear_curve(curve1, curve2, tx, "angle"))
        else:
            val = sg.LinearRing(I_Helper.linear_curve(curve1, curve2, tx, "distance"))
        
        return mg.TS_LinearRing(val, time, start_ts.crs)
        
        
class I_Helper:
    
    @staticmethod
    def linear_point(p1, p2, t):
        """
        Args:
            p1 (tuple): tuple with 2 or 3 elements representing the x,y,z-coordinates
            p2 (tuple): tuple with 2 or 3 elements representing the x,y,z-coordinates
            t (float): value between 0 and 1 defining the position between p1 and p2 for the return point
            
        Returns:
            tuple: returns tuple with 2 or 3 elements representing the x,y,z-coordinates between p1 and p2 at t
            
        Raises:
            ValueError: if len(p1) and len(p2) is not equal
        """
        if len(p1) != len(p2) or len(p1) != 2 and len(p1) != 3:
            raise ValueError(text.IHelper_Texts.lp_error1)
        
        t_x = (1 - t)*p1[0] + t*p2[0]
        t_y = (1 - t)*p1[1] + t*p2[1]
        
        if len(p1) == 3:
            t_z = (1 - t)*p1[2] + t*p2[2]
            return (t_x, t_y, t_z)
        else:
            return (t_x, t_y)
        
    @staticmethod
    def z_dictance(p1, p2):
        """calculates distance between two points with, taking the z-coordinate into consideration
        
        Args:
            p1 (tuple): Tuple with three elements representing the x,y,z-coordinates
            p2 (tuple): Tuple with three elements representing the x,y,z-coordinates
            
        Returns:
            float: returns distance between the two points
        """
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)
    
    @staticmethod
    def angle(p1, p2, p3, use_z=False):
        """Calculates angle between segment p1p2 and p2p3
        
        Args:
            p1 (tuple): tuple with 2 or 3 elements representing the x,y,z-coordinates
            p2 (tuple): tuple with 2 or 3 elements representing the x,y,z-coordinates
            p3 (tuple): tuple with 2 or 3 elements representing the x,y,z-coordinates
            use_z (bool): if true, z-coordinates are taken into calculation
            
        Returns:
            float: returns angle in degree
            
        Raises:
            ValueError: if len(p1), len(p2) and len(p3) is not equal
        """
        
        if len(p1) != len(p2) or len(p2) != len(p3) or len(p1) != 2 and len(p1) != 3:
            raise ValueError(text.IHelper_Texts.ang_error1)
        
        if len(p1) == 2 or use_z is False:
            d_p1_p2 = sg.LineString([p1, p2]).length
            d_p1_p3 = sg.LineString([p1, p3]).length
            d_p2_p3 = sg.LineString([p2, p3]).length
            
        else:
            d_p1_p2 = I_Helper.z_dictance(p1, p2)
            d_p1_p3 = I_Helper.z_dictance(p1, p3)
            d_p2_p3 = I_Helper.z_dictance(p2, p3)
        
        if d_p1_p2 + d_p2_p3 == d_p1_p3:
            return 0.0
        else:
            return round(math.degrees(math.acos((d_p1_p3**2 - d_p2_p3**2 - d_p1_p2**2)/(2*d_p2_p3*d_p1_p2))), 10)
    
    @staticmethod
    def line_distance(p1, p2, p3):
        """Calculates distance of p2 to line p1,p3
        
        Note:
            distance calculation takes only x- and y-coordinates into account
            
        Args:
            p1 (tuple): tuple with 2 or 3 elements representing the x,y,z-coordinates
            p2 (tuple): tuple with 2 or 3 elements representing the x,y,z-coordinates
            p3 (tuple): tuple with 2 or 3 elements representing the x,y,z-coordinates
            
        Returns:
            float: returns distance of p2 to line p1,p3
        """
        l = sg.LineString([p1,p3])
        p = sg.Point(p2)
        
        return p.distance(l)
    
    @staticmethod
    def angle_to_x_axis(p1, p2):
        """Calculates angle of line defined by p1 and p2, to x-axis
            -> if y of p2 < y of p1 -> angle > 180 degree
            
        Note:
            only x- and y- coordiantes are taken into calculation
                
        Args:
            p1 (tuple): tuple with 2 or 3 elements representing the x,y,z-coordinates
            p2 (tuple): tuple with 2 or 3 elements representing the x,y,z-coordinates
            
        Returns:
            float: Angle to x_axis
        """
        p1 = p1[:2]
        p2 = p2[:2]
        p3 = (p1[0] + 1.0, p1[1])
        
        ang = 180 - I_Helper.angle(p3, p1, p2)
        if p2[1] < p1[1]:
            ang = 360.0 - ang
            
        return ang
        
    @staticmethod
    def linear_curve(curve1, curve2, time, s_type="angle"):
        """linear interpolation between two shapely.geometry.LineStrings
        
        Note:
            only x- and y- coordinates are used for line simplification
        
        Args:
            curve1 (shapely.geometry.LineString): LineString at t1
            curve2 (shapely.geometry.LineString): LineString at t2
            time (float): float between 0.0 and 1.0 defining the point between t1 and t2 for which LineString will be interpolated
            s_type (string): defines line simplification type: 'angle' or 'distance'
            
        Returns:
            shapely.geometry.LineString: returns LineString at 'time'
        """
        
        if len(curve1.coords) == len(curve2.coords):
            return sg.LineString([I_Helper.linear_point(curve1.coords[i], curve2.coords[i], time) for i in range(len(curve1.coords[:]))])
        
        elif len(curve1.coords) > len(curve2.coords):
            base_coords = curve1.coords[:]
            fill_coords = curve2.coords[:]
            
        elif len(curve1.coords) < len(curve2.coords):
            base_coords = curve2.coords[:]
            fill_coords = curve1.coords[:]
        
        s_list = I_Helper.basic_simplify(copy.deepcopy(base_coords), len(fill_coords), s_type)
        
        # retrieve deleted points
        line_index = []
        del_index = []
        del_i = 0
        for i in range(len(base_coords)):
            if base_coords[i] == s_list[del_i]:
                line_index.append(i)
                del_i += 1
            else:
                del_index.append(i)
                
        new_line = copy.deepcopy(fill_coords)
        # adding coordinates to new_line
        del_index.sort(reverse=True)
        for i in del_index:
            next_i = bisect.bisect_left(line_index, i)
            prev_i = next_i - 1
            next_c = line_index[next_i]
            prev_c = line_index[prev_i]
                
            part_seg_len = sg.LineString(base_coords[prev_c:i+1]).length
            full_seg_len = sg.LineString(base_coords[prev_c:next_c+1]).length
            t = part_seg_len/full_seg_len
            new_point = I_Helper.linear_point(fill_coords[prev_i], fill_coords[next_i], t)
            new_line.insert(next_i, new_point)
        
        if len(curve1.coords) > len(curve2.coords):
            return sg.LineString([I_Helper.linear_point(base_coords[i], new_line[i], time) for i in range(len(new_line))])
        
        elif len(curve1.coords) < len(curve2.coords):
            return sg.LineString([I_Helper.linear_point(new_line[i], base_coords[i], time) for i in range(len(new_line))])
        
    @staticmethod
    def curve_segments(curve):
        """
        Args:
            curve (shapely.geometry.LineString): linestring for which list of segments will be created
            
        Returns:
            list: Returns list curve segments that are represented as point pairs
                -> curve = [(1,1),(2,1),(2,2)]
                -> segments = [[(1,1),(2,1)],[(2,1),(2,2)]]
        """
        curve_seg = []
        
        curve = curve.coords[:]
        
        for i,p in enumerate(curve[1:]):
            curve_seg.append([curve[i],p])
            
        return curve_seg
    
    @staticmethod
    def linestring_from_segments(curve_segments):
        """Creates LineString from curve segments
        
        Args:
            curve_segments (list): list with curve segments (length of each segment does not necessarly have to be two)
                -> [[(1,1), (2,1)], [(2,1),(2,4),(3,5),(3,4)],[...]]
                
        Returns:
            shapely.geometry.LineString
        """
        curve_segments = copy.deepcopy(curve_segments)
        line_list = [p for p in curve_segments[0]]
        del curve_segments[0]
        
        for seg in curve_segments:
            for s in seg[1:]:
                line_list.append(s)
                
        return sg.LineString(line_list)
        
    @staticmethod
    def create_diff_dict(convex, non_convex):
        """creates dictionary containing differences between convex and non_convex LinearRings
        
        Note:
            only differences in the 2-dimensional coordinate space are taken into account
        
        Args:
            convex (list): list of segments of convex linear ring
            non_convex (list): list of segments of non-convex linear ring
            
        Returns:
            dict: Returns dictionary containing elements of non_convex linear ring that are not part of the convex linear ring
                The dict has the following structure: {0:[(2,3),(2,5),(1,4)], 3:[(4,3),(4,1)]}, where the key defines the index of the segment
                in the convex polygon and the value are the coordinates of a linestring
        """
        non_convex = copy.deepcopy(non_convex)
        # match starting points of convex and non_convex linestring
        while convex[0][0] != non_convex[0][0]:
            non_convex.append(non_convex[0])
            del non_convex[0]
        
        # creating diff dict
        diff_dict = {}  
        for i, seg in enumerate(convex):
            
            if seg == non_convex[0]:
                del non_convex[0]
                continue
            else:
                
                diff_dict[i] = []
                
                while len(non_convex) > 0 and non_convex[0][0] != seg[1]:
                    diff_dict[i].append(non_convex[0])
                    del non_convex[0]
                    
        diff_dict = {key:I_Helper.linestring_from_segments(diff_dict[key]).coords[:] for key in diff_dict}
        
        return diff_dict
    
    @staticmethod
    def basic_simplify(curve, n, s_type="angle"):
        """
        reduces the number of control points in curve to n
        
        Args:
            curve(list of tuples): list of tuples holding coordinate values
            n (int): number of control points of returned curve
            
        Returns:
            list of tuples representing simplified linestring
        """
        if len(curve) <= n or len(curve) <= 2:
            return curve
        
        if s_type == "angle":
            v_list = [(i,I_Helper.angle(curve[i-1],
                                     curve[i],
                                     curve[i+1],
                                     use_z=False)) for i in range(1, len(curve)-1)]
            
        elif s_type == "distance":
            v_list = [(i,I_Helper.line_distance(curve[i-1],
                                             curve[i],
                                             curve[i+1])) for i in range(1, len(curve)-1)]
            
        v_list.sort(key=lambda x: x[1])
        del curve[v_list[0][0]]
        
        return I_Helper.basic_simplify(curve, n, s_type)
    