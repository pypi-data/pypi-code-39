# -*- coding: utf-8 -*-
"""
This module contains the following classes of the "sptemp"-package:

    TS_Geometry
    TS_Point
    TS_LineString
    TS_LinearRing
    Moving_Geometry
    Moving_Point
    Moving_LineString
    Moving_LinearRing
    Moving_Collection
    Moving_Polygon
    Moving_MultiPoint
    Moving_MultiLineString
    Moving_MultiPoylgon

Todo:
    - Implementation of reprojection functionality
"""

import copy
import inspect
import functools
import datetime as dt
from abc import ABCMeta

import shapely.geometry as sg
import shapely.ops as so

from sptemp import zeit
from sptemp import _texts as text


class TS_Geometry(zeit.TS_Object):
    """With this class timestamped shapely.geometry objects can be represented.
    This class is a subclass of the sptemp.zeit.TS_Object class and inherits all its attributes and methods
    
    >>> TS_Geometry(shapely.geometry.Point(10.2, 47.4, 460), datetime.datetime(2017, 07, 25, 20, 0, 0), crs=pyproj.Proj(init="epsg:4326"))
    
    Attributes:
        value (shapely.geometry): Geometry that is timestamped.
        ts (datetime.datetime or sptemp.zeit.Time_Period): timestamp value -> immutable
        type (type): type of the value the TS_Geometry represents
        has_z (bool): True if value.has_z is True
        crs (pyproj.Proj or NoneType): returns coordinate reference system of the Geometry
    """
    
    def __init__(self, value, ts, crs=None):
        """
        Args:
            value (shapely.geometry): Geometry that is timestamped.
            ts (datetime.datetime or sptemp.zeit.Time_Period): timestamp for value
            crs (pyproj.Proj, optional): coordinate reference system of the TS_Geometry
            
        Raises:
            TypeError: if value is not of type shapely.geometry OR ts is not of type datetime.datetime or sptemp.zeit.Time_Period
                OR crs is not of type pyproj.Proj
            ValueError: if shapely.geometry.is_empty is True
        """
        sg_classes = [x[1] for x in inspect.getmembers(sg, inspect.isclass)]
        sg_classes.remove(sg.CAP_STYLE)
        sg_classes.remove(sg.JOIN_STYLE)
        if type(value) not in [x[1] for x in inspect.getmembers(sg, inspect.isclass)]:
            raise TypeError(text.TS_Geometry_Texts.init_error1)
        
        elif value.is_empty:
            raise ValueError(text.TS_Geometry_Texts.init_error2)
        
        elif crs is not None:
            # import pyproj here so package can be used without pyproj
            import pyproj
            
            if isinstance(crs, pyproj.Proj) is False:
                raise TypeError(text.TS_Geometry_Texts.init_error3)
        
        super(TS_Geometry, self).__init__(value, ts)
        
        self._has_z = self._value.has_z
        self._crs = copy.deepcopy(crs)
    
    @property
    def value(self):
        return copy.deepcopy(self._value)
        
    @value.setter
    def value(self, value):
        if isinstance(value, self._type) is False:
            raise TypeError(text.TS_Geometry_Texts.v_error1)
        
        elif self._has_z is not value.has_z:
            raise ValueError(text.TS_Geometry_Texts.v_error2)
        
        else:
            self._value = copy.deepcopy(value)
            
    @property
    def has_z(self):
        return self._has_z
    
    @property
    def crs(self):
        return copy.deepcopy(self._crs)
    
    def __eq__(self, another):
        """Checks if the TS_Geometry is equal to another TS_Geometry
        
        Note:
            This method will not raise an error when 'another' is not of type sptemp.zeit.TS_Geometry
            but instead will return False
        
        Args:
            another(sptemp.zeit.TS_Point): another TS_Geometry
            
        Returns:
            bool: Returns True if another.value == value AND another.ts == ts AND another.crs == self.crs, else returns False
        """
        if isinstance(another, self.__class__) is False:
            return False
        
        elif self.value != another.value or self.ts != another.ts:
            return False
        
        elif self._crs is not None and another.crs is None or self._crs is None and another.crs is not None:
            return False
        
        elif self._crs is not None and another.crs is not None:
            if self._crs.srs == another.crs.srs:
                return True
            else:
                return False
            
        else:
            return True
        
    def reproject(self, to_crs):
        """Transforms self.value into new coordinate system
        
        Args:
            to_crs (pyproj.Proj): coordinate reference system to which the coordinates of the geometry are converted to
        
        Raises:
            TypeError: if to_crs is not of type pyproj.Proj
            ValueError: if TS_Geometry has no coordinate reference system
        """
        
        if self._crs is None:
            raise ValueError(text.TS_Geometry_Texts.r_error1)
        
        import pyproj
        
        if isinstance(to_crs, pyproj.Proj) is False:
            raise TypeError(text.TS_Geometry_Texts.r_error2)
        
        project = functools.partial(pyproj.transform, self._crs, to_crs)
        self._value = so.transform(project, self._value)
        
        self._crs = copy.deepcopy(to_crs)
    
        
class Moving_Geometry(zeit.Moving_Object):
    """
    Abstract class that defines methods for all moving_geometry types.
    The class is a subclass of the sptemp.zeit.Moving_Object class and inherits all its attributes and methods.
    
    Attributes:
        interpolator (sptemp.zeit.Interpolator): Interpolator associated with the Moving_Geometry
        has_z (boolean): True if all TS_Geometries in Moving_Geometry have z-coordinates, else False.
        crs (pyproj.Proj or NoneType): coordinate reference system of the Ts_Geometries
    """
    
    __metaclass__ = ABCMeta
    
    @property
    def has_z(self):
        return self._has_z
    
    @property
    def crs(self):
        return copy.deepcopy(self._crs)
    
    def within(self, another, td1, td2, args1=None, args2=None):
        """
        Tests at which points in time the Moving_Geometry lays within 'another' geometry.
        
        Args:
            another (shapely.geometry or TS_Geometry or Moving_Geometry or Moving_Collection): Geometry for which it will be checked if Moving_Geometry lays within.
            td1 (datetime.timedelta): timedelta object defining at which temporal resolution, the predicate 'within' is checked
            td2 (datetime.timedelta): timedelta object defining at which temporal resolution, changes of the predicate 'within' will be checked
            args1 (sptemp.zeit.Moving_Object, optional): Moving Objects holding timestamped args values, defining which args are passed to interpolator of moving_geometry at which times.
                Moving_Object must hold timestamped lists, which contain the args.
            args2 (sptemp.zeit.Moving_Object, optional): Moving Objects holding timestamped args values, defining which args are passed to interpolator of another at which times.
                Moving_Object should hold timestamped lists, which hold the args, if isintance(another, Moving_Geometry). |br|
                Moving_Object should hold timestamped dicts, which hold the args, if isintance(another, Moving_Collection). With the dict complying to the specifications of the
                Moving_Collection.interpolate() method.
                
        Returns:
            sptemp.zeit.Moving_Object: returns Moving_object with type == bool.
            The Moving_Object represents the points in time at which the Moving_Geometry lays within 'another'.
            Returned Moving_Object is assigned a constant interpolation
        
        Raises:
            TypeError: If type(another) not in [shapely.geometry, TS_Geometry, Moving_Geometry, Moving_Collection]
            ValueError: If td1 or td2 are not positive or if td2 > td1
        """
        if td1 < dt.timedelta(microseconds=1) or td2 < dt.timedelta(microseconds=1):
            raise ValueError(text.MG_Texts.w_error2)
        
        elif td1 < td2:
            raise ValueError(text.MG_Texts.w_error3)
        
        from sptemp.interpolation import ICollection as IC
        ip = zeit.Interpolator([zeit.TS_Unit(IC.constant, zeit.Time_Period(self.start_time(), self.end_time()))])
        
        t = self.start_time()
        end_t = self.end_time()
        return_list = []
        
        sg_classes = [x[1] for x in inspect.getmembers(sg, inspect.isclass)]
        sg_classes.remove(sg.CAP_STYLE)
        sg_classes.remove(sg.JOIN_STYLE)
        
        def _get_self_val(ti):
            return self.interpolate(ti, *args1.interpolate(ti).value) if args1 and args1.interpolate(ti) else self.interpolate(ti)
        
        def _get_another_val(ti):
            if type(another) in sg_classes:
                return another
            
            elif isinstance(another, TS_Geometry):
                return None if ti < another.start_time() or ti > another.end_time() else another.value
            
            elif isinstance(another, Moving_Geometry):
                if args2 and args2.interpolate(ti):
                    if another.interpolate(ti, *args2.interpolate(ti).value):
                        return another.interpolate(ti, *args2.interpolate(ti).value).value
                    else:
                        return None
                else:
                    if another.interpolate(ti):
                        return another.interpolate(ti)
                    else:
                        return None
            
            elif isinstance(another, Moving_Collection):
                if args2 and args2.interpolate(ti):
                    if another.interpolate(ti, args2.interpolate(ti).value):
                        return another.interpolate(ti, args2.interpolate(ti).value).value
                    else:
                        return None
                    
                else:
                    if another.interpolate(ti):
                        return another.interpolate(ti).value
                    else:
                        return None
                    
            else:
                raise TypeError(text.MG_Texts.w_error1)
                
        control = True
        while control:
            self_val = _get_self_val(t)
            another_val = _get_another_val(t)
            predicate = self_val.value.within(another_val) if self_val and another_val else False
            
            if t >= end_t:
                t = end_t
                control = False
            
            if predicate:
                if len(return_list) == 0:
                    return_list.append(zeit.TS_Object(True,t))
                    
                elif return_list[-1].value is False:
                    
                    c_t = t - td1 if t - td1 > return_list[-1].ts else return_list[-1].ts
                    control2 = True
                    while control2:
                        if c_t >= end_t:
                            c_t = end_t
                            control2 = False
                        
                        s_v = _get_self_val(c_t)
                        a_v = _get_another_val(c_t)
                        
                        if s_v is None or a_v is None or s_v.value.within(a_v) is False:
                            c_t += td2
                        else:
                            return_list.append(zeit.TS_Object(True,c_t))
                            break
            
            else:
                if len(return_list) == 0:
                    return_list.append(zeit.TS_Object(False,t))
                    
                elif return_list[-1].value is True:
                    
                    c_t = t - td1 if t - td1 > return_list[-1].ts else return_list[-1].ts
                    control2 = True
                    while control2:
                        if c_t >= end_t:
                            c_t = end_t
                            control2 = False
                            
                        s_v = _get_self_val(c_t)
                        a_v = _get_another_val(c_t)
                        
                        if s_v is None or a_v is None or s_v.value.within(a_v) is False:
                            return_list.append(zeit.TS_Object(False,c_t))
                            break
                        else:
                            c_t += td2
                            
            t += td1
        
        if return_list[-1].ts != self.end_time():
            last_item = zeit.TS_Object(return_list[-1].value, self.end_time())
            return_list.append(last_item)
            
        return zeit.Moving_Object(return_list, ip)
    
    def reproject(self, to_crs):
        """Transforms TS_Geometry objects in Moving_Geometry to new coordinate system
         
        Args:
            to_crs (pyproj.Proj): coordinate reference system to which the Point coordinates are converted to
             
        Raises:
            TypeError: if to_crs is not of type pyproj.Proj
            ValueError: if self.crs is None
        """
        if self._crs is None:
            raise ValueError(text.MP_Texts.re_error1)
         
        for tsg in self._ts_object_list:
            tsg.reproject(to_crs)
         
        self._crs = copy.deepcopy(to_crs)
    

class TS_Point(TS_Geometry):
    """Instances of this class represent a timestamped shapely.geometry.Point.
    This class is a subclass of the TS_Geometry class and inherits all its attributes and methods.
    
    Attributes:
        value (shapely.geometry.Point): Point that is timestamped.
        ts (datetime.datetime or sptemp.zeit.Time_Period): timestamp value -> immutable
        type (type): type of the value the TS_Point represents -> shapely.geometry.Point
        has_z (bool): True if value.has_z is True
        crs (pyproj.Proj or NoneType): returns coordinate reference system of the Point
    """
    
    def __init__(self, value, ts, crs=None):
        """
        >>> tsp1 = TS_Point(shapely.geometry.Point(20.4, 10.8, 560), datetime.datetime(2018, 07, 25, 18, 31, 23), pyproj.Proj(init="epsg:4326"))
        
        Args:
            value (shapely.geometry.Point): Point that is timestamped.
            ts (datetime.datetime or sptemp.zeit.Time_Period): timestamp for value
            crs (pyproj.Proj, optional): coordinate reference system of the Point
            
        Raises:
            TypeError: if value is not of type shapely.geometry.Point OR ts is not of type datetime.datetime or sptemp.zeit.Time_Period
                OR crs is not of type pyproj.Proj
            ValueError: if shapely.geometry.Point.is_empty is True
        """
        if isinstance(value, sg.Point) is False:
            raise TypeError(text.TS_Point_Texts.init_error1)
        
        TS_Geometry.__init__(self, value, ts, crs)
        
        self._has_z = self._value.has_z
        self._crs = copy.deepcopy(crs)


class Moving_Point(Moving_Geometry):
    """With this class a sequence of TS_Points can be represented.
    The class is a subclass of the Moving_Geometry class and inherits all its attributes and methods.
    
    Attributes:
        interpolator (sptemp.zeit.Interpolator): Interpolator associated with the Moving_Point
        has_z (boolean): True if all TS_Points in Moving Point have z-coordinates, else False.
        crs (pyproj.Proj or NoneType): coordinate reference system of the Ts_Points
    """
    def __init__(self, ts_object_list, interpolator):
        """
        Args:
            ts_object_list (list of sptemp.zeit.TS_Point): time-sorted list of disjoint TS_Point instances
            Interpolator (sptemp.zeit.Interpolator): Interpolator object that will be used to interpolate values of Moving_Point.
            
        Raises:
            TypeError: if ts_object_list is not of type list OR ts_object_list contains objects that are nor of type sptemp.moving_geometry.TS_Point
                OR interpolator is not of type sptemp.zeit.Interpolator
            ValueError: if len(ts_object_list) == 0 OR if timestamps of TS_Points are not disjoint OR TS_Point.has_z of objects in ts_object_list
                is inconsistent OR TS_Point.crs of objects in ts_object_list is inconsistent.
        """
        super(Moving_Point, self).__init__(ts_object_list, interpolator)
        
        for tsp in ts_object_list:
            
            if isinstance(tsp, TS_Point) is False:
                raise TypeError(text.MP_Texts.init_error1)
            
            elif tsp.crs is None and ts_object_list[0].crs is not None or tsp.crs is not None and ts_object_list[0].crs is None:
                raise ValueError(text.MP_Texts.init_error2)
            
            elif tsp.crs and tsp.crs.srs != ts_object_list[0].crs.srs:
                raise ValueError(text.MP_Texts.init_error2)
            
            elif tsp.has_z is not ts_object_list[0].has_z:
                raise ValueError(text.MP_Texts.init_error3)
            
        self._has_z = ts_object_list[0].has_z
        self._crs = copy.deepcopy(ts_object_list[0].crs)
        
    @property
    def has_z(self):
        return self._has_z
    
    @property
    def crs(self):
        return copy.deepcopy(self._crs)
    
    def __setitem__(self, key, value):
        """
        Args:
            key (int): the index
            value (sptemp.moving_geometry.TS_Point): new TS_Point
            
        Raises:
            TypeError: If key is not of type integer OR if value is not of type sptemp.moving_geometry.TS_Point
            IndexError: If key is out of range
            ValueError: If value.ts is not disjoint to existing Ts_Points in Moving_Point 
                OR TS_Point.has_z != self.has_z OR value.crs != self.crs
        """
        if isinstance(value, TS_Point) is False:
            raise TypeError(text.MP_Texts.set_error1)
        
        MG_Helper.has_z_equal(self.has_z, value.has_z)
        
        MG_Helper.crs_equal(self._crs, value.crs)
        
        super(Moving_Point, self).__setitem__(key, value)
    
    def append(self, value):
        """
        Args:
            value (sptemp.zeit.TS_Point): TS_Point that will be appended to Moving_Point
        
        Raises:
            TypeError: If value is not of type sptemp.zeit.TS_Point
            ValueError: If value.start_time() <= Moving_Object.end_time() OR value.has_z != self.has_z OR value.crs != self.crs
        """
        if isinstance(value, TS_Point) is False:
            raise TypeError(text.MP_Texts.app_error1)
        
        MG_Helper.has_z_equal(self.has_z, value.has_z)
        
        MG_Helper.crs_equal(self._crs, value.crs)
        
        super(Moving_Point, self).append(value)
        
    def insert(self, value):
        """Insert value into Moving_Point
        
        Note:
            In contrary to Interpolator objects -> Values will not be overwritten or adjusted
            
        Args:
            value (sptemp.zeit.TS_Point): TS_Point that will be inserted into Moving_Point
        
        Raises:
            TypeError: If value is not of type sptemp.zeit.TS_Point
            ValueError: If value.ts and timestamps of TS_Objects in Moving_Point are not disjoint
                or if value.type != self.type OR value.has_z != self.has_z OR value.crs != self.crs
        """
        if isinstance(value, TS_Point) is False:
            raise TypeError(text.MP_Texts.in_error1)
        
        MG_Helper.has_z_equal(self.has_z, value.has_z)
        
        MG_Helper.crs_equal(self._crs, value.crs)
        
        super(Moving_Point, self).insert(value)
        
        
class TS_LineString(TS_Geometry):
    """Instances of this class represent a timestamped shapely.geometry.LineString.
    The class is a subclass of the TS_Geometry class and inherits all its attributes and methods
    
    Attributes:
        value (shapely.geometry.LineString): LineString that is timestamped.
        ts (datetime.datetime or sptemp.zeit.Time_Period): timestamp value -> immutable
        type (type): type of the value the TS_LineString represents -> shapely.geometry.LineString
        has_z (bool): True if value.has_z is True
        crs (pyproj.Proj or NoneType): returns coordinate reference system of the LineString
    """
    
    def __init__(self, value, ts, crs=None):
        """
        Args:
            value (shapely.geometry.LineString): LineString that is timestamped.
            ts (datetime.datetime or sptemp.zeit.Time_Period): timestamp for the value
            crs (pyproj.Proj, optional): coordinate reference system of the LineString
            
        Raises:
            TypeError: if value is not of type shapely.geometry.LineString OR ts is not of type datetime.datetime or sptemp.zeit.Time_Period
                OR crs is not of type pyproj.Proj
            ValueError: if shapely.geometry.LineString.is_empty is True
        """
        if isinstance(value, sg.LineString) is False:
            raise TypeError(text.TS_LineString_Texts.init_error1)
        
        TS_Geometry.__init__(self, value, ts, crs)
        
        self._has_z = self._value.has_z
        self._crs = copy.deepcopy(crs)
        
        
class Moving_LineString(Moving_Geometry):
    """With this class a sequence of TS_LineStrings can be represented.
    The class is a subclass of the Moving_Geometry class and inherits all its attributes and methods.
    
    Attributes:
        interpolator (sptemp.zeit.Interpolator): Interpolator associated with the Moving_LineString
        has_z (boolean): True if all TS_LineStrings in Moving_LineString have z-coordinates, else False.
        crs (pyproj.Proj or NoneType): coordinate reference system of the TS_LineStrings
    """
    def __init__(self, ts_object_list, interpolator):
        """
        Args:
            ts_object_list (list of sptemp.zeit.TS_LineString): time-sorted list of disjoint TS_LineString instances
            Interpolator (sptemp.zeit.Interpolator): Interpolator object that will be used to interpolate values of Moving_LineString.
            
        Raises:
            TypeError: if ts_object_list is not of type list OR if ts_object_list contains objects that are nor of type sptemp.zeit.TS_LineString
                or interpolator is not of type sptemp.zeit.Interpolator
            ValueError: if len(ts_object_list) == 0 OR TS_LineStrings do not all have the same type OR if timestamps of TS_LineString are not disjoint
        """
        super(Moving_LineString, self).__init__(ts_object_list, interpolator)
        
        for tsl in ts_object_list:
            
            if isinstance(tsl, TS_LineString) is False:
                raise TypeError(text.ML_Texts.init_error1)
            
            elif tsl.crs is None and ts_object_list[0].crs is not None or tsl.crs is not None and ts_object_list[0].crs is None:
                raise ValueError(text.ML_Texts.init_error2)
            
            elif tsl.crs and tsl.crs.srs != ts_object_list[0].crs.srs:
                raise ValueError(text.ML_Texts.init_error2)
            
            elif tsl.has_z is not ts_object_list[0].has_z:
                raise ValueError(text.ML_Texts.init_error3)
            
        self._has_z = ts_object_list[0].has_z
        self._crs = copy.deepcopy(ts_object_list[0].crs)
        
    @property
    def has_z(self):
        return self._has_z
    
    @property
    def crs(self):
        return copy.deepcopy(self._crs)
    
    def __setitem__(self, key, value):
        """
        Args:
            key (int): the index
            value (sptemp.moving_geometry.TS_LineString): new TS_LineSTring
            
        Raises:
            TypeError: If key is not of type integer, if value is not of type sptemp.moving_geometry.TS_LineString
            IndexError: If key is out of range
            ValueError: If value.ts is not disjoint to existing Ts_Points in Moving_LineString 
                OR TS_Point.has_z != self.has_z OR value.crs != value.crs
        """
        if isinstance(value, TS_LineString) is False:
            raise TypeError(text.ML_Texts.set_error1)
        
        MG_Helper.has_z_equal(self.has_z, value.has_z)
        
        MG_Helper.crs_equal(self._crs, value.crs)
        
        super(Moving_LineString, self).__setitem__(key, value)
    
    def append(self, value):
        """
        Args:
            value (sptemp.zeit.TS_LineString): TS_LineString that will be appended to Moving_LineString
        
        Raises:
            TypeError: If value is not of type sptemp.zeit.TS_LineString
            ValueError: If value.start_time() <= Moving_Object.end_time() OR value.has_z != self.has_z OR value.crs != self.crs
        """
        if isinstance(value, TS_LineString) is False:
            raise TypeError(text.ML_Texts.app_error1)
        
        MG_Helper.has_z_equal(self.has_z, value.has_z)
        
        MG_Helper.crs_equal(self._crs, value.crs)
        
        super(Moving_LineString, self).append(value)
        
    def insert(self, value):
        """Insert value into Moving_LineString
        
        Note:
            In contrary to Interpolator objects -> Values will not be overwritten or adjusted
            
        Args:
            value (sptemp.zeit.TS_LineString): TS_LineString that will be inserted into Moving_LineString
        
        Raises:
            TypeError: If value is not of type sptemp.zeit.TS_LineString
            ValueError: If value.ts and timestamps of Ts_Objects in Moving Object are not disjoint
                or if value.type != self.type OR value.has_z != self.has_z OR value.crs != self.crs
        """
        if isinstance(value, TS_LineString) is False:
            raise TypeError(text.ML_Texts.in_error1)
        
        MG_Helper.has_z_equal(self.has_z, value.has_z)
        
        MG_Helper.crs_equal(self._crs, value.crs)
        
        super(Moving_LineString, self).insert(value)
        
        
class TS_LinearRing(TS_LineString):
    """Instances of this class represent a timestamped shapely.geometry.LinearRing.
    The class is a subclass of the TS_LineString class and inherites all its attributes and methods
    
    Attributes:
        value (shapely.geometry.LinearRing): LinearRing that is timestamped.
        ts (datetime.datetime or sptemp.zeit.Time_Period): timestamp value -> immutable
        type (type): type of the value the TS_LinearRing represents -> shapely.geometry.LinearRing
        has_z (bool): True if value.has_z is True
        crs (pyproj.Proj or NoneType): returns coordinate reference system of the LinearRing
    """
    
    def __init__(self, value, ts, crs=None):
        """
        Args:
            value (shapely.geometry.LinearRing): LinearRing that is timestamped.
            ts (datetime.datetime or sptemp.zeit.Time_Period): timestamp for value
            crs (pyproj.Proj, optional): coordinate reference system of the LinearRing
            
        Raises:
            TypeError: if value is not of type shapely.geometry.LinearRing OR ts is not of type datetime.datetime or sptemp.zeit.Time_Period
                OR crs is not of type pyproj.Proj
            ValueError: if shapely.geometry.LinearRing.is_empty is True
        """
        if isinstance(value, sg.LinearRing) is False:
            raise TypeError(text.TS_LinearRing_Texts.init_error1)
        
        TS_LineString.__init__(self, value, ts, crs)
        
        self._has_z = self._value.has_z
        self._crs = copy.deepcopy(crs)
        
        
class Moving_LinearRing(Moving_LineString):
    """With this class a sequence of TS_LinearRings can be represented.
    The class is a subclass of the Moving_LineString class and inherits all its attributes and methods.
    
    Attributes:
        interpolator (sptemp.zeit.Interpolator): Interpolator associated with the Moving_LinearRing
        has_z (boolean): True if all TS_LinearRings in Moving_LinearRing have z-coordinates, else False.
        crs (pyproj.Proj or NoneType): coordinate reference system of the TS_LinearRings
    """
    def __init__(self, ts_object_list, interpolator):
        """
        Args:
            ts_object_list (list of sptemp.zeit.TS_LinearRing): time-sorted list of disjoint TS_LinearRing instances
            Interpolator (sptemp.zeit.Interpolator): Interpolator object that will be used to interpolate values of Moving_LinearRing.
            
        Raises:
            TypeError: if ts_object_list is not of type list ,if ts_object_list contains objects that are nor of type sptemp.zeit.TS_LinearRing
                or interpolator is not of type sptemp.zeit.Interpolator
            ValueError: if len(ts_object_list) == 0 OR TS_LinearRings do not all have the same type OR if timestamps of TS_LinearRing are not disjoint
        """
        super(Moving_LinearRing, self).__init__(ts_object_list, interpolator)
        
        for tslr in ts_object_list:
            
            if isinstance(tslr, TS_LinearRing) is False:
                raise TypeError(text.MLR_Texts.init_error1)
            
            elif tslr.crs is None and ts_object_list[0].crs is not None or tslr.crs is not None and ts_object_list[0].crs is None:
                raise ValueError(text.MLR_Texts.init_error2)
            
            elif tslr.crs and tslr.crs.srs != ts_object_list[0].crs.srs:
                raise ValueError(text.MLR_Texts.init_error2)
            
            elif tslr.has_z is not ts_object_list[0].has_z:
                raise ValueError(text.MLR_Texts.init_error3)
            
        self._has_z = ts_object_list[0].has_z
        self._crs = copy.deepcopy(ts_object_list[0].crs)
        
    def __setitem__(self, key, value):
        """
        Args:
            key (int): the index
            value (sptemp.moving_geometry.TS_LineString): new TS_LinearRing
            
        Raises:
            TypeError: If key is not of type integer, if value is not of type sptemp.moving_geometry.TS_LinearRing
            IndexError: If key is out of range
            ValueError: If value.ts is not disjoint to existing Ts_Points in Moving_LinearRing
                OR TS_Point.has_z != self.has_z OR value.crs != value.crs
        """
        if isinstance(value, TS_LinearRing) is False:
            raise TypeError(text.MLR_Texts.set_error1)
        
        MG_Helper.has_z_equal(self.has_z, value.has_z)
        
        MG_Helper.crs_equal(self._crs, value.crs)
        
        super(Moving_LineString, self).__setitem__(key, value)
    
    def append(self, value):
        """
        Args:
            value (sptemp.zeit.TS_LinearRing): TS_LinearRing that will be appended to Moving_LinearRing
        
        Raises:
            TypeError: If value is not of type sptemp.zeit.TS_LinearRing
            ValueError: If value.start_time() <= Moving_Object.end_time() OR value.has_z != self.has_z OR value.crs != self.crs
        """
        if isinstance(value, TS_LinearRing) is False:
            raise TypeError(text.MLR_Texts.app_error1)
        
        MG_Helper.has_z_equal(self.has_z, value.has_z)
        
        MG_Helper.crs_equal(self._crs, value.crs)
        
        super(Moving_LinearRing, self).append(value)
        
    def insert(self, value):
        """Insert value into Moving_LinearRing
        
        Note:
            In contrary to Interpolator objects -> Values will not be overwritten or adjusted
            
        Args:
            value (sptemp.zeit.TS_LinearRing): TS_LinearRing that will be inserted into Moving_LinearRing
        
        Raises:
            TypeError: If value is not of type sptemp.zeit.TS_LinearRing
            ValueError: If value.ts and timestamps of Ts_Objects in Moving Object are not disjoint
                or if value.type != self.type OR value.has_z != self.has_z OR value.crs != self.crs
        """
        if isinstance(value, TS_LinearRing) is False:
            raise TypeError(text.MLR_Texts.in_error1)
        
        MG_Helper.has_z_equal(self.has_z, value.has_z)
        
        MG_Helper.crs_equal(self._crs, value.crs)
        
        super(Moving_LinearRing, self).insert(value)
        
        
class Moving_Collection(object):
    """With this class a collection of moving geometries can be represented.
    
    Note:
        Objects stored in the collection are not copied. The user must manage the objects in the Moving_Collection.moving_list
        
    Attributes:
        moving_list (list): List of objects stored in Moving_Collection
        has_z (boolean): True if all objects in collection have z-coordinates, else False.
        crs (pyproj.Proj or NoneType): coordinate reference system of the objects stored in the collection
    """
    def __init__(self, moving_list):
        """
        Args:
            moving_list (list): List of objects of the types: Moving_Point, Moving_LineString and MovingPolygon
            
        Raises:
            ValueError: If moving_list is empty, if 'has_z' or 'crs' is not consistent among objects of moving_list .
            TypeError: If moving list is not of type list OR object in moving_list is not of type:
                Moving_Point, Moving_LineString or MovingPolygon.
        """
        if not moving_list:
            raise ValueError(text.MC_Texts.init_error1)
        
        elif isinstance(moving_list, list) is False:
            raise TypeError(text.MC_Texts.init_error2)
        
        for mv in moving_list:
            if isinstance(mv, Moving_Point) is False and isinstance(mv, Moving_LineString) is False and isinstance(mv, Moving_Polygon) is False:
                raise TypeError(text.MC_Texts.init_error3)
            
            MG_Helper.has_z_equal(mv.has_z, moving_list[0].has_z)
            MG_Helper.crs_equal(mv.crs, moving_list[0].crs)
        
        self.moving_list = moving_list
        self.has_z = moving_list[0].has_z
        self.crs = moving_list[0].crs
        
    def interpolate(self, time, args_dict={}):
        """
        Args:
            time (datetime.datetime): point in time for which value of Moving_Collection will be returned
            args_dict (dict, optional): dictionary with arbitrary arguments that will be passed 
                to Interpolators of objects stored in collection. Keys in dictionary must correspond to position of objects
                in the Moving_Collection.moving_list. For Moving_Points and Moving_LineStrings the value should be a list holding the additional arguments,
                while for Moving_Polygons the value in the args_dict should be another args_dict, specifying which args should be passed to which
                LinearRing of the Moving_Polygon. 
            
        Returns:
            sptemp.moving_geometry.TS_Geometry or NoneType: Returns TS_Geometry with GeometryCollection as value and 'time' as timestamp.
            Returns None if time < self.start_time() or time > self.end_time() or interpolation function of all Moving_Geometries returned None
        
        Raises:
            TypeError: if type time is not datetime.datetime OR type arg_dict is not of type dict
            ValueError: if crs of Moving_Collection is inconsistent
        """
        if isinstance(time, dt.datetime) is False:
            raise TypeError(text.MC_Texts.ip_error1)
        
        elif isinstance(args_dict, dict) is False:
            raise TypeError(text.MC_Texts.ip_error2)
        
        c_list = []
        for i, mo in enumerate(self.moving_list):
            MG_Helper.crs_equal(self.crs, mo.crs)
            
            if isinstance(mo, Moving_Polygon):
                arg = args_dict[i] if i in args_dict else None
                mo_t = mo.interpolate(time, arg) if arg else mo.interpolate(time)
            else:
                arg = args_dict[i] if i in args_dict else None
                mo_t = mo.interpolate(time, *arg) if arg else mo.interpolate(time)
                
            if mo_t:
                c_list.append(mo_t.value)
                
        if c_list:
            return TS_Geometry(sg.GeometryCollection(c_list), time, self.crs)
        else:
            return None  
    
    def slice(self, time):
        """
        Args:
            time (sptemp.zeit.Time_Period): Time_Period for which the slice will be created.
            
        Returns:
            sptemp.zeit.Moving_Collection or NoneType: Calls slice method of all objects in Moving_Collection
            returns None if all slice of all objects in the collection are None
            
        Raises:
            TypeError: if type(time) != sptemp.zeit.Time_Period
        """
        if isinstance(time, zeit.Time_Period) is False:
            raise TypeError(text.MC_Texts.slice_error1)
        
        elif time.end < self.start_time() or time.start > self.end_time():
            return None
        
        c_list = []
        
        for mo in self.moving_list:
            sl = mo.slice(time)
            if sl:
                c_list.append(sl)
                
        if c_list:
            return self.__class__(c_list)
        else:
            return None
        
    def resampled_slice(self, times, time_args={}):
        """
        Call resampled slice method of all object in the Moving_Collection
        
        Args:
            times (list of datetime.datetime): List of time instants
            time_args (dict): dictionary holding index of moving_geometry in moving_list as key and Moving_Object
                that defines which additional arguments are passed to Interpolator at which points in time.
                For Moving_Polygons the value must be a dictionary holding the time_args Moving _Object for each 
                Moving_LinearRing.
            
        Returns:
            sptemp.zeit.Moving_Collection or NoneType: Returns resampled-slice of original Moving_Collection
            returns None if resampled_slice method of all items in Moving_Collection return None
            
        Raises:
            TypeError: if type of times is not list OR if type interpolator_dict is not of type dict
            ValueError: if len(times) < 2
        """
        if isinstance(times, list) is False:
            raise TypeError(text.MC_Texts.re_slice_error1)
        
        if len(times) < 2:
            raise ValueError(text.MC_Texts.re_slice_error2)
        
        elif times[-1] < self.start_time() or times[0] > self.end_time():
            return None
        
        c_list = []
        
        for i,mo in enumerate(self.moving_list):
            if i in time_args:
                sl = mo.resampled_slice(times, time_args[i])
            else:
                sl = mo.resampled_slice(times)
            if sl:
                c_list.append(sl)
                
        if c_list:
            return self.__class__(c_list)
        else:
            return None
        
    def start_time(self):
        """
        Returns:
            datetime.datetime: Returns smallest start_time of all objects in Moving_Collection.moving_list
        """
        return min([x.start_time() for x in self.moving_list])
    
    def end_time(self):
        """
        Returns:
            datetime.datetime: Returns largest end_time of all objects in Moving_Collection.moving_list
        """
        return max([x.end_time() for x in self.moving_list])
    
    def reproject(self, to_crs):
        """Transforms objects in moving_list into new coordinate reference system
         
        Args:
            to_crs (pyproj.Proj): coordinate reference system to which the coordinates are converted to
             
        Raises:
            TypeError: if to_crs is not of type pyproj.Proj
            ValueError: if self.crs is None
        """
        for mo in self.moving_list:
            mo.reproject(to_crs)
             
        self.crs = to_crs
    
    
class Moving_Polygon(Moving_Collection):
    """With this class a collection of Moving_LinearRings can be represented which represent the rings of a moving polygon
    
    Note:
        Objects stored in the collection are not copied. The user must manage the Moving_LinearRings of the Moving_Polygon
        
    Attributes:
        exterior_ring (sptemp.moving_geometry.Moving_LinearRing): exterior ring of the Moving_Polygon
        interior_rings (list of sptemp.moving_geometry.Moving_LinearRing, optional): interior rings of the Moving_Polygon
        has_z (boolean): True if all objects in collection have z-coordinates, else False.
        crs (pyproj.Proj or NoneType): coordinate reference system of the objects stored in the collection
    """
    
    def __init__(self, exterior_ring, interior_rings=[]):
        """
        Args:
           exterior_ring (sptemp.moving_geometry.Moving_LinearRing): exterior ring of the Moving_Polygon
           interior_rings (list of sptemp.moving_geometry.Moving_LinearRing, optional): interior rings of the Moving_Polygon
           
        Raises:
            TypeError: if exterior_ring is not of type sptemp.moving_geometry.Moving_LinearRing OR
                interior_rings is not of type list OR
                interior_rings contains elements that are not of type sptemp.moving_geometry.Moving_LinearRing
        """
        if isinstance(exterior_ring, Moving_LinearRing) is False:
            raise TypeError(text.MPL_Texts.init_error1)
        
        if isinstance(interior_rings, list) is False:
            raise TypeError(text.MPL_Texts.init_error2)
        
        for mlr in interior_rings:
            
            if isinstance(mlr, Moving_LinearRing) is False:
                raise TypeError(text.MPL_Texts.init_error3)
            
            MG_Helper.has_z_equal(mlr.has_z, exterior_ring.has_z)
            MG_Helper.crs_equal(mlr.crs, exterior_ring.crs)
        
        self.exterior_ring = exterior_ring
        self.interior_rings = interior_rings
        self.has_z = exterior_ring.has_z
        self.crs = exterior_ring.crs
        
    def interpolate(self, time, args_dict={}):
        """
        Args:
            time (datetime.datetime): point in time for which value of Moving_Polygon will be returned
            args_dict (dict, optional): dictionary holding arbitrary arguments for the Interpolators of the Moving_LinearRings
                stored in the collection. The args of the exterior ring should be stored under the key 'exterior'
                The args for the interior rings should have the index of the LinearRing in the interior_rings list as key.
            
        Returns:
            sptemp.moving_geometry.TS_Geometry or NoneType: Returns TS_Geometry with Polygon as value and 'time' as timestamp.
            Returns None if time < self.start_time() or time > self.end_time() or interpolation function of exterior_ring returned None.
        
        Raises:
            TypeError: if type time is not of type datetime.datetime OR type of arg_dict is not dict
            ValueError: if crs of Moving_Polygon is inconsistent
        """
        if isinstance(time, dt.datetime) is False:
            raise TypeError(text.MPL_Texts.ip_error1)
        
        elif isinstance(args_dict, dict) is False:
            raise TypeError(text.MPL_Texts.ip_error2)
        
        if "exterior" in args_dict:
            ext = self.exterior_ring.interpolate(time, args_dict["exterior"])
        else:
            ext = self.exterior_ring.interpolate(time)
            
        if ext is None:
            return None
            
        interior_list = []
        for i, mlr in enumerate(self.interior_rings):
            MG_Helper.crs_equal(self.crs, mlr.crs)
            arg = args_dict[i] if i in args_dict else None
            mlr_t = mlr.interpolate(time, arg) if arg else mlr.interpolate(time)
            if mlr_t:
                interior_list.append(mlr_t.value.coords[:])
                
        return TS_Geometry(sg.Polygon(ext.value.coords[:], interior_list), time, self.crs)
    
    def slice(self, time):
        """
        Args:
            time (sptemp.zeit.Time_Period): Time_Period for which the slice will be created
            
        Returns:
            sptemp.zeit.Moving_Polygon or NoneType: Calls slice method of all objects in Moving_Polygon.
            Returns None if slice of all objects in the collection returned None
            
        Raises:
            TypeError: if type(time) != sptemp.zeit.Time_Period
            ValueError: if slice does not include any TS_LinearRings of the exterior ring
        """
        if isinstance(time, zeit.Time_Period) is False:
            raise TypeError(text.MPL_Texts.slice_error1)
        
        ext_slice = self.exterior_ring.slice(time)
            
        if ext_slice is None:
            return None
        
        int_list = []
        
        for mlr in self.interior_rings:
            sl = mlr.slice(time)
            
            if sl:
                int_list.append(sl)
        
        return Moving_Polygon(ext_slice, int_list)
    
    def resampled_slice(self, times, time_args={}):
        """
        Returns Moving_Polygon, holding the resampled_slices of all Moving_LinearRings
        
        Args:
            times (list of datetime.datetime): List of time instants
            time_args (dict): Dictionary holding Moving_Objects as values, defining which additional arguments are passed
                to the Interpolators of the Moving_LinearRings at which points in time. For the exterior_ring the key must be
                'exterior', for the interior rings, the key must be the index of the Moving_LinearRing in the interior_rings list.
            
        Returns:
            sptemp.zeit.Moving_Polygon or NoneType: Returns Moving_Polygon, holding the resampled_slices of all Moving_LinearRings.
            Returns None of resampled_slice method of all Moving_LinearRings returned None.
            
        Raises:
            TypeError: if type of times is not list
            ValueError: if len(times) < 2
        """
        if isinstance(times, list) is False:
            raise TypeError(text.MC_Texts.re_slice_error1)
        
        if len(times) < 2:
            raise ValueError(text.MC_Texts.re_slice_error2)
        
        elif times[-1] < self.start_time() or times[0] > self.end_time():
            return None
        
        if "exterior" in time_args:
            ext_slice = self.exterior_ring.resampled_slice(times, time_args["exterior"])
        else:
            ext_slice = self.exterior_ring.resampled_slice(times)
            
        if ext_slice is None:
            return None
        
        int_list = []
        
        for i,mlr in enumerate(self.interior_rings):
            if i in time_args:
                sl = mlr.resampled_slice(times, time_args[i])
            else:
                sl = mlr.resampled_slice(times)
            if sl:
                int_list.append(sl)
        
        return Moving_Polygon(ext_slice, int_list)
        
    def start_time(self):
        """
        Returns:
            datetime.datetime: Returns start_time of exterior_ring
        """
        return self.exterior_ring.start_time()
    
    def end_time(self):
        """
        Returns:
            datetime.datetime: Returns end_time of exterior_ring
        """
        return self.exterior_ring.end_time()
    
    def reproject(self, to_crs):
        """Transforms coordinates of Moving_LinearRings into new coordinate reference system
         
        Args:
            to_crs (pyproj.Proj): coordinate reference system to which the coordinates are converted to
             
        Raises:
            TypeError: if to_crs is not of type pyproj.Proj
            ValueError: if self.crs is None
        """
        self.exterior_ring.reproject(to_crs)
        for mlr in self.interior_rings:
            mlr.reproject(to_crs)
             
        self.crs = to_crs
        

class Moving_MultiPoint(Moving_Collection):
    """With this class a collection of Moving_Points can be represented
    
    Note:
        Objects stored in the collection are not copied. The user must manage the objects in the Moving_Point.moving_list
        
    Attributes:
        moving_list (list): List of Moving_Point-objects
        has_z (bool): True if all objects in collection have z-coordinates, else False.
        crs (pyproj.Proj or NoneType): coordinate reference system of the objects stored in the collection
    
    """
    def __init__(self, moving_list):
        """
        Args:
            moving_list (list): List of Moving_Point-objects
            
        Raises:
            ValueError: If moving_list is empty, if 'has_z' or 'crs' is not consistent among objects of moving_list .
            TypeError: If moving list is not of type list OR object in moving_list is not of type Moving_Point
        """
        if not moving_list:
            raise ValueError(text.MMP_Texts.init_error1)
        
        elif isinstance(moving_list, list) is False:
            raise TypeError(text.MMP_Texts.init_error2)
        
        for mv in moving_list:
            if isinstance(mv, Moving_Point) is False:
                raise TypeError(text.MMP_Texts.init_error3)
            
            MG_Helper.has_z_equal(mv.has_z, moving_list[0].has_z)
            MG_Helper.crs_equal(mv.crs, moving_list[0].crs)
        
        self.moving_list = moving_list
        self.has_z = moving_list[0].has_z
        self.crs = moving_list[0].crs
        
    def interpolate(self, time, args_dict={}):
        """
        Args:
            time (datetime.datetime): point in time for which value of Moving_MultiPoint will be returned
            args_dict (dict, optional): dictionary with arbitrary arguments that will be passed 
                to Interpolators of objects stored in collection. Keys in dictionary must correspond to position of objects
                in the Moving_MultiPoint.moving_list. The value should be a list holding the additional arguments. 
            
        Returns:
            sptemp.moving_geometry.TS_Geometry or NoneType: Returns TS_Geometry with shapely.geometry.MultiPoint as value and 'time' as timestamp.
            Returns None if time < self.start_time() or time > self.end_time() or interpolation function of all Moving_Points returned None
        
        Raises:
            TypeError: if type time is not datetime.datetime OR type arg_dict is not of type dict
            ValueError: if crs of Moving_MultiPoint is inconsistent
        """
        ip_v = super(Moving_MultiPoint, self).interpolate(time, args_dict)
        if ip_v is None:
            return None
        else:
            return TS_Geometry(sg.MultiPoint(ip_v.value), time, self.crs)
        

class Moving_MultiLineString(Moving_Collection):
    """With this class a collection of Moving_LineStrings can be represented
    
    Note:
        Objects stored in the collection are not copied. The user must manage the objects in the Moving_MultiLineString.moving_list
        
    Attributes:
        moving_list (list): List of objects stored in Moving_MultiLineString
        has_z (boolean): True if all objects in collection have z-coordinates, else False.
        crs (pyproj.Proj or NoneType): coordinate reference system of the objects stored in the collection
    
    """
    def __init__(self, moving_list):
        """
        Args:
            moving_list (list): List of Moving_LineString-objects
            
        Raises:
            ValueError: If moving_list is empty, if 'has_z' or 'crs' is not consistent among objects of moving_list .
            TypeError: If moving list is not of type list OR object in moving_list is not of type Moving_LineString
        """
        if not moving_list:
            raise ValueError(text.MML_Texts.init_error1)
        
        elif isinstance(moving_list, list) is False:
            raise TypeError(text.MML_Texts.init_error2)
        
        for mv in moving_list:
            if isinstance(mv, Moving_LineString) is False:
                raise TypeError(text.MML_Texts.init_error3)
            
            MG_Helper.has_z_equal(mv.has_z, moving_list[0].has_z)
            MG_Helper.crs_equal(mv.crs, moving_list[0].crs)
        
        self.moving_list = moving_list
        self.has_z = moving_list[0].has_z
        self.crs = moving_list[0].crs
        
    def interpolate(self, time, args_dict={}):
        """
        Args:
            time (datetime.datetime): point in time for which value of Moving_MultiLineString will be returned
            args_dict (dict, optional): dictionary with arbitrary arguments that will be passed 
                to Interpolators of objects stored in collection. Keys in dictionary must correspond to position of objects
                in the Moving_MultiLineString.moving_list. The value should be a list holding the additional arguments. 
            
        Returns:
            sptemp.moving_geometry.TS_Geometry or NoneType: Returns TS_Geometry with MultiLineString as value and 'time' as timestamp.
            Returns None if time < self.start_time() or time > self.end_time() or interpolation function of all Moving_LineString returned None
        
        Raises:
            TypeError: if type time is not datetime.datetime OR type arg_dict is not of type dict
            ValueError: if crs of Moving_MultiLineString is inconsistent
        """
        ip_v = super(Moving_MultiLineString, self).interpolate(time, args_dict)
        if ip_v is None:
            return None
        else:
            return TS_Geometry(sg.MultiLineString(ip_v.value), time, self.crs)
        
        
class Moving_MultiPolygon(Moving_Collection):
    """With this class a collection of Moving_Polygons can be represented
    
    Note:
        Objects stored in the collections are not copied. The user must manage the objects in the Moving_MultiPolygon.moving_list
        
    Attributes:
        moving_list (list): List of objects stored in Moving_MultiPolygon
        has_z (boolean): True if all objects in collection have z-coordinates, else False.
        crs (pyproj.Proj or NoneType): coordinate reference system of the objects stored in the collection
    """
    def __init__(self, moving_list):
        """
        Args:
            moving_list (listof sptemp.moving_geometry.Moving_Polygon): List of Moving_Polygon-objects
            
        Raises:
            ValueError: If moving_list is empty, if 'has_z' or 'crs' is not consistent among objects of moving_list .
            TypeError: If moving list is not of type list OR object in moving_list is not of type Moving_Polygon
        """
        if not moving_list:
            raise ValueError(text.MMPL_Texts.init_error1)
        
        elif isinstance(moving_list, list) is False:
            raise TypeError(text.MMPL_Texts.init_error2)
        
        for mv in moving_list:
            if isinstance(mv, Moving_Polygon) is False:
                raise TypeError(text.MMPL_Texts.init_error3)
            
            MG_Helper.has_z_equal(mv.has_z, moving_list[0].has_z)
            MG_Helper.crs_equal(mv.crs, moving_list[0].crs)
        
        self.moving_list = moving_list
        self.has_z = moving_list[0].has_z
        self.crs = moving_list[0].crs
        
    def interpolate(self, time, args_dict={}):
        """
        Args:
            time (datetime.datetime): point in time for which value of Moving_MultiPoint will be returned
            args_dict (dict, optional): dictionary with arbitrary arguments that will be passed 
                to Interpolators of objects stored in collection. Keys in dictionary must correspond to position of objects
                in the Moving_MultiPolygon.moving_list. The value should be a dictionary, defining which additional arguments are passed to which
                Moving_LinearRing of the Moving_Polygon.
            
        Returns:
            sptemp.moving_geometry.TS_Geometry or NoneType: Returns TS_Geometry with MultiPolygon as value and 'time' as timestamp.
            Returns None if time < self.start_time() or time > self.end_time() or interpolation function of all Moving_Points returned None
        
        Raises:
            TypeError: if type time is not datetime.datetime OR type arg_dict is not of type dict
            ValueError: if crs of Moving_MultiPolygon is inconsistent
        """
        ip_v = super(Moving_MultiPolygon, self).interpolate(time, args_dict)
        if ip_v is None:
            return None
        else:
            return TS_Geometry(sg.MultiPolygon(ip_v.value), time, self.crs)

    
class MG_Helper:
    
    @staticmethod
    def has_z_equal(has_z1, has_z2):
        """
        Args:
            has_z1 (boolean): has_z value 1
            has_z2 (boolean): has_z value 2
            
        Raises:
            ValueError: If has_z1 != has_z2
        """
        if has_z1 is not has_z2:
            raise ValueError(text.MG_Helper_Texts.hz_error1)
        
    @staticmethod
    def crs_equal(crs1, crs2):
        """
        Args:
            crs1 (pyproj.Proj or NoneType): crs value 1
            crs2 (pyproj.Proj or NoneType): crs value 2
            
        Raises:
            ValueError: If crs1 != crs2
        """
        if crs1 is None and crs2 is not None or crs1 is not None and crs2 is None:
                raise ValueError(text.MG_Helper_Texts.crs_error1)
            
        elif crs1 and crs1.srs != crs2.srs:
            raise ValueError(text.MG_Helper_Texts.crs_error1)
        
    