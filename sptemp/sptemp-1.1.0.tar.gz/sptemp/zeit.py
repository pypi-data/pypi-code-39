# -*- coding: utf-8 -*-
"""
This module contains the following classes of the "sptemp"-package:
    
    Time_Period
    TS_Object
    TS_Unit
    Interpolator
    Moving_Object

ToDo:
"""
import datetime as dt
import types
import copy
import bisect

from sptemp import _texts as text

class Time_Period(object):
    """ This class can be used to represent time periods with a closed lower and closed upper border.
    
    >>> tp1 = Time_Period(datetime.datetime(2017, 07, 25, 20, 0, 0), datetime.datetime(2017, 07, 25, 20, 0, 20))
    >>> tp2 = Time_Period(datetime.datetime(2017, 07, 25, 20, 0, 25), datetime.datetime(2017, 07, 25, 20, 0, 45))
    
    Attributes:
        start (datetime.datetime): start time instant of the time_period
        end (datetime.datetime): end time instant of the time_period
    """
    
    def __init__(self, start, end):
        """
        Args:
            start (datetime.datetime): start time_instant of the time_period
            end (datetime.datetime): end time_instant of the time_period
            
        Raises:
            TypeError: if start or end is not of type datetime.datetime
            ValueError: if start is larger or equal to end
        """
        if isinstance(start, dt.datetime) is False or isinstance(end, dt.datetime) is False:
            raise TypeError(text.TP_Texts.init_error1)
        
        elif start >= end:
            raise ValueError(text.TP_Texts.init_error2)
        
        self._start = start
        self._end = end
    
    @property
    def start(self):
        return self._start
    
    @start.setter
    def start(self, time):
        if isinstance(time, dt.datetime) is False:
            raise TypeError(text.TP_Texts.start_error1)
            
        elif time >= self._end:
            raise ValueError(text.TP_Texts.start_error2)
        
        else:
            self._start = time
            
    @property    
    def end(self):
        return self._end
    
    @end.setter
    def end(self, time):
        if isinstance(time, dt.datetime) is False:
            raise TypeError(text.TP_Texts.start_error1)
            
        elif time <= self._start:
            raise ValueError(text.TP_Texts.start_error1)
        
        else:
            self._end = time
            
    @classmethod
    def from_iso(cls, start, end):
        """
        >>> tp1 = Time_Period.from_iso("2017-07-25T22:00:00", "2017-07-25T22:00:20")
        
        Args:
            start (string): start time_instant of the time_period in the iso8601 format
            end (string): end time_instant of the time_period in the iso8601 format
            
        Raises:
            ValueError: if start is larger or equal to end
            
        Returns:
            sptemp.zeit.Time_Period:
        """
        start = ZeitHelper.parse_time_from_iso(start)
        end = ZeitHelper.parse_time_from_iso(end)
        
        return cls(start, end) 
            
    def __lt__(self, another):
        """Checks if Time_Period lays before a time instant or a Time_Period
        
        >>> tp1 < tp2
        True
        
        Args:
            another(datetime.datetime or sptemp.zeit.Time_Period): another Time_Period or a time instant
            
        Returns:
            bool: If type(another) == datetime.datetime -> returns True if self.end < another, else returns False.
            If type(another) == sptemp.zeit.Time_Period -> returns True if self.end < another.start, else returns False
                  
        Raises:
            TypeError: If type(another) != datetime.datetime AND type(another) != sptemp.zeit.Time_Period
        """
        return self.before(another)
    
    def __gt__(self, another):
        """Checks if Time_Period lays after a time instant or a Time_Period
        
        >>> tp1 > tp2
        False
        
        Args:
            another(datetime.datetime or sptemp.zeit.Time_Period): another Time_Period or a time instant
            
        Returns:
            bool: If type(another) == datetime.datetime -> returns True if self.start > another, else returns False.
            If type(another) == sptemp.zeit.Time_Period -> returns True if self.start > another.end, else returns False
                  
        Raises:
            TypeError: If type(another) != datetime.datetime AND type(another) != sptemp.zeit.Time_Period
        """
        return self.after(another)
        
    def __eq__(self, another):
        """Checks if Time_Period is equal to another Time_Period
        
        Note:
            This method will not raise an error when 'another' is not of type sptemp.zeit.Time_Period
            but instead will return False
        
        Args:
            another(sptemp.zeit.Time_Period): another Time_Period
            
        Returns:
            bool: Returns True if another.start == self.start AND another.end == self.end, else returns False
        """
        if isinstance(another, self.__class__) is False:
            return False
        
        elif self.start != another.start or self.end != another.end:
            return False
        
        else:
            return True
    
    def __ne__(self, another):
        """Checks if Time_Period is not equal to another Time_Period
        
        Note:
            This method will not raise an error when 'another' is not of type sptemp.zeit.Time_Period
            but instead will return True
        
        Args:
            another(sptemp.zeit.Time_Period): another Time_Period
            
        Returns:
            bool: Returns True if another.start != self.start OR another.end != self.end, else returns True
        """
        return not self.__eq__(another)
    
    def before(self, another):
        """Checks if Time_Period lays before a time instant or a Time_Period 
        
        Args:
            another(datetime.datetime or sptemp.zeit.Time_Period): another Time_Period or a time instant
            
        Returns:
            bool: If type(another) == datetime.datetime -> returns True if self.end < another, else returns False.
            If type(another) == sptemp.zeit.Time_Period -> returns True if self.end < another.start, else returns False
                  
        Raises:
            TypeError: If type(another) != datetime.datetime AND type(another) != sptemp.zeit.Time_Period
        """
        if isinstance(another, dt.datetime):
            if self.end < another:
                return True
            else:
                return False
            
        elif isinstance(another, self.__class__):
            if self.end < another.start:
                return True
            else:
                return False
        
        else:
            raise TypeError(text.TP_Texts.general_error1)
        
    def after(self, another):
        """Checks if Time_Period lays after a time instant or a Time_Period 
        
        Args:
            another(datetime.datetime or sptemp.zeit.Time_Period): another Time_Period or a time instant
            
        Returns:
            bool: If type(another) == datetime.datetime -> returns True if self.start > another, else returns False.
            If type(another) == sptemp.zeit.Time_Period -> returns True if self.start > another.end, else returns False
                  
        Raises:
            TypeError: If type(another) != datetime.datetime AND type(another) != sptemp.zeit.Time_Period
        """
        if isinstance(another, dt.datetime):
            if self.start > another:
                return True
            else:
                return False
            
        elif isinstance(another, self.__class__):
            if self.start > another.end:
                return True
            else:
                return False
        
        else:
            raise TypeError(text.TP_Texts.general_error1)
        
    def contains(self, another):
        """Checks if Time_Period contains a time instant or a Time_Period 
        
        Args:
            another(datetime.datetime or sptemp.zeit.Time_Period): another Time_Period or a time instant
            
        Returns:
            bool: If type(another) == datetime.datetime -> returns True if self.start < another AND self.end > another, else returns False.
            If type(another) == sptemp.zeit.Time_Period -> returns True if self.start < another.start and self.end > another.end, else returns False
                  
        Raises:
            TypeError: If type(another) != datetime.datetime AND type(another) != sptemp.zeit.Time_Period
        """
        if isinstance(another, dt.datetime):
            if self.start < another and self.end > another:
                return True
            else:
                return False
            
        elif isinstance(another, self.__class__):
            if self.start < another.start and self.end > another.end:
                return True
            else:
                return False
            
        else:
            raise TypeError(text.TP_Texts.general_error1)
        
    def includes(self, another):
        """Checks if Time_Period includes a time instant or a Time_Period 
        
        Args:
            another(datetime.datetime or sptemp.zeit.Time_Period): another Time_Period or a time instant
            
        Returns:
            bool: If type(another) == datetime.datetime -> returns True if self.start <= another AND self.end >= another, else returns False.
            If type(another) == sptemp.zeit.Time_Period -> returns True if self.start <= another.start and self.end >= another.end, else returns False
                  
        Raises:
            TypeError: If type(another) != datetime.datetime AND type(another) != sptemp.zeit.Time_Period
        """
        if isinstance(another, dt.datetime):
            if self.start <= another and self.end >= another:
                return True
            else:
                return False
            
        elif isinstance(another, self.__class__):
            if self.start <= another.start and self.end >= another.end:
                return True
            else:
                return False
            
        else:
            raise TypeError(text.TP_Texts.general_error1)
        
    def meets(self, another):
        """Checks if Time_Period meets a time instant or a Time_Period 
        
        Args:
            another(datetime.datetime or sptemp.zeit.Time_Period): another Time_Period or a time instant
            
        Returns:
            bool: If type(another) == datetime.datetime -> returns True if self.end == another, else returns False.
            If type(another) == sptemp.zeit.Time_Period -> returns True if self.end == another.start, else returns False
                  
        Raises:
            TypeError: If type(another) != datetime.datetime AND type(another) != sptemp.zeit.Time_Period
        """
        if isinstance(another, dt.datetime):
            if self.end == another:
                return True
            else:
                return False
            
        elif isinstance(another, self.__class__):
            if self.end == another.start:
                return True
            else:
                return False
            
        else:
            raise TypeError(text.TP_Texts.general_error1)
        
    def metBy(self, another):
        """Checks if Time_Period is met by a time instant or a Time_Period 
        
        Args:
            another(datetime.datetime or sptemp.zeit.Time_Period): another Time_Period or a time instant
            
        Returns:
            bool: If type(another) == datetime.datetime -> returns True if self.start == another, else returns False.
            If type(another) == sptemp.zeit.Time_Period -> returns True if self.start == another.end, else returns False
                  
        Raises:
            TypeError: If type(another) != datetime.datetime AND type(another) != sptemp.zeit.Time_Period
        """
        if isinstance(another, dt.datetime):
            if self.start == another:
                return True
            else:
                return False
            
        elif isinstance(another, self.__class__):
            if self.start == another.end:
                return True
            else:
                return False
            
        else:
            raise TypeError(text.TP_Texts.general_error1)
        
    def equals(self, another):
        """Checks if Time_Period is equal to another Time_Period
        
        Args:
            another(sptemp.zeit.Time_Period): another Time_Period
            
        Returns:
            bool: Returns True if another.start == self.start AND another.end == self.end, else returns False.
            
        Raises:
            TypeError: if another is not of type sptemp.zeit.Time_Period
        """
        if isinstance(another, self.__class__) is False:
            raise TypeError(text.TP_Texts.general_error2)
        
        elif self.start != another.start or self.end != another.end:
            return False
        
        else:
            return True
        
    def during(self, another):
        """Checks if Time_Period is lays during another Time_Period
        
        Args:
            another(sptemp.zeit.Time_Period): another Time_Period
            
        Returns:
            bool: Returns True if another.contains(self), else returns False.
            
        Raises:
            TypeError: if another is not of type sptemp.zeit.Time_Period
        """
        if isinstance(another, self.__class__) is False:
            raise TypeError(text.TP_Texts.general_error2)
        
        elif another.contains(self):
            return True
        
        else:
            return False
        
    def overlaps(self, another):
        """Checks if Time_Period overlaps another Time_Period
        
        Args:
            another(sptemp.zeit.Time_Period): another Time_Period
            
        Returns:
            bool: Returns True if self.start < another.start AND self.end > another.start AND self.end < another.end, else returns False.
            
        Raises:
            TypeError: if another is not of type sptemp.zeit.Time_Period
        """
        if isinstance(another, self.__class__) is False:
            raise TypeError(text.TP_Texts.general_error2)
        
        elif self.start < another.start and self.end > another.start and self.end < another.end:
            return True
        
        else:
            return False
        
    def overlappedBy(self, another):
        """Checks if Time_Period is overlapped by another Time_Period
        
        Args:
            another(sptemp.zeit.Time_Period): another Time_Period
            
        Returns:
            bool: Returns True if another.overlaps(self), else returns False.
            
        Raises:
            TypeError: if another is not of type sptemp.zeit.Time_Period
        """
        if isinstance(another, self.__class__) is False:
            raise TypeError(text.TP_Texts.general_error2)
        
        elif another.overlaps(self):
            return True
        
        else:
            return False
        
        
class TS_Object(object):
    """With this class timestamped objects can be represented.
    Any type of object can be timestamped with a datetime.datetime object
    or a sptemp.zeit.Time_Period object.
    
    >>> ts1 = TS_Object(10, datetime.datetime(2018, 07, 25, 18, 31, 23))
    >>> ts2 = TS_Object(True, Time_Period(datetime.datetime(1999, 04, 21, 7, 22, 50),datetime.datetime(1999, 04, 21, 7, 22, 55)))
    
    Attributes:
        value (object): value that is timestamped.
            Raises TypeError if new value is assigned that is not of the same type of the old value.
        ts (datetime.datetime or sptemp.zeit.Time_Period): timestamp value -> immutable
        type (type): type of the value, the TS_Object represents -> immutable
    """
    def __init__(self, value, ts):
        """
        Args:
            value (object): Object value to be timestamped
            ts (datetime.datetime or sptemp.zeit.Time_Period): timestamp for value
            
        Raises:
            TypeError: if ts is not of type datetime.datetime or sptemp.zeit.Time_Period
        """
        if isinstance(ts, dt.datetime) is False and isinstance(ts, Time_Period) is False:
            raise TypeError(text.TS_Texts.init_error1)
        
        self._value = copy.deepcopy(value)
        self._ts = copy.deepcopy(ts)
        self._type = type(value)
    
    @property
    def value(self):
        return copy.deepcopy(self._value)
        
    @value.setter
    def value(self, value):
        if isinstance(value, self._type):
            self._value = copy.deepcopy(value)
        else:
            raise TypeError(text.TS_Texts.v_error1)
        
    @property
    def ts(self):
        return copy.deepcopy(self._ts)

    @property
    def type(self):
        return copy.deepcopy(self._type)
    
    def __eq__(self, another):
        """Checks if the TS_Object is equal to another TS_Object
        
        >>> ts1 == ts2
        False
        
        Note:
            This method will not raise an error when 'another' is not of type sptemp.zeit.TS_Object
            but instead will return False
        
        Args:
            another(sptemp.zeit.TS_Object): another TS_Object
            
        Returns:
            bool: Returns True if another.value == value AND another.ts == ts, else returns False
        """
        if isinstance(another, self.__class__) is False:
            return False
        
        elif self.value != another.value or self.ts != another.ts:
            return False
        
        else:
            return True
        
    def __ne__(self, another):
        """Checks if the TS_Object is not equal to another TS_Object
        
        >>> ts1 != ts2
        True
        
        Note:
            This method will not raise an error when 'another' is not of type sptemp.zeit.TS_Object
            but instead will return True
        
        Args:
            another(sptemp.zeit.TS_Object): another TS_Object
            
        Returns:
            bool: Returns True if another.value != value or another.ts != ts, else returns False
        """
        return not self.__eq__(another)
    
    def start_time(self):
        """Returns the start time instant of the TS_Object
        -> if type(self.ts) == datetime.datetime
        -> self.start_time == self.end_time
        
        Returns:
            datetime.datetime: Returns the start time instant of the TS_Object
        """
        if isinstance(self.ts, dt.datetime):
            return self.ts
        else:
            return self.ts.start
        
    def end_time(self):
        """Returns the end time instant of the TS_Object
        -> if type(self.ts) == datetime.datetime
        -> self.start_time == self.end_time
        
        Returns:
            datetime.datetime: Returns the end time instant of the TS_Object
        """
        if isinstance(self.ts, dt.datetime):
            return self.ts
        else:
            return self.ts.end


class TS_Unit(TS_Object):
    """Instances of this class represent a timestamped function.
    The class is a subclass of the sptemp.zeit.TS_Object class and inherits all attributes and methods
    
    >>> tsu1 = TS_Unit(ICollection.linear,
    ... Time_Period(datetime.datetime(2017, 07, 25, 20, 0, 0), datetime.datetime(2017, 07, 25, 20, 0, 20)))
    
    Attributes:
        value (types.FuntionType): function that is timestamped.
        ts (sptemp.zeit.Time_Period): timestamp value -> immutable
        type (type): type of the value the TS_Object represents -> immutable
    """
    
    def __init__(self, value, ts):
        """
        Args:
            value (types.FuntionType): Object value to be timestamped
            ts (sptemp.zeit.Time_Period): timestamp for value
            
        Raises:
            TypeError: if value is not of type types.FuntionType OR ts is not of type sptemp.zeit.Time_Period
        """
        if isinstance(value, types.FunctionType) is False:
            raise TypeError(text.Unit_Texts.init_error1)
        
        elif isinstance(ts, Time_Period) is False:
            raise TypeError(text.Unit_Texts.init_error2)
        
        self._value = value
        self._ts = ts
        self._type = type(value)
        
    def interpolate(self, start_ts, end_ts, time, *args):
        """Calls function assigned to TS_Unit to interpolate value based on start_ts and end_ts at time instant 'time'
        
        >>> tsp1 = TS_Object(10.0, datetime.datetime(2017, 07, 25, 20, 0, 5))
        >>> tsp2 = TS_Object(20.0, datetime.datetime(2017, 07, 25, 20, 0, 15))
        >>> tsu1.interpolate(tsp1, tsp2, datetime.datetime(2017, 07, 25, 20, 0, 7))
        TS_Object(12.0, datetime.datetime(2017, 07, 25, 20, 0, 7))
        
        Args:
            start_ts (sptemp.zeit.TS_Object): previous TS_Object of time
            end_ts (sptemp.zeit.TS_Object): next TS_Object of time
            time (datetime.datetime): time for which value will be interpolated
            *args: arbitrary arguments that will be passed into interpolation function
        
        Returns:
            sptemp.zeit.TS_Object or NoneType: returns TS_Object with the value beeing the interpolated value
            
        Raises:
            TypeError: if start_ts or end_ts is not of type sptemp.zeit.TS_Object
                OR if time is not of type datetime.datetime
            ValueError: if self.ts does not include start_ts.end
                OR if self.ts does not include time
        """
        if isinstance(start_ts, TS_Object) is False or isinstance(end_ts, TS_Object) is False:
            raise TypeError(text.Unit_Texts.i_error1)
        
        elif isinstance(time, dt.datetime) is False:
            raise TypeError(text.Unit_Texts.i_error2)
        
        elif self.ts.includes(start_ts.end_time()) is False:
            raise ValueError(text.Unit_Texts.i_error3)
        
        elif self.ts.includes(time) is False:
            raise ValueError(text.Unit_Texts.i_error5)
        
        if args:
            i_val = self.value(start_ts, end_ts, time, *args)
        else:
            i_val = self.value(start_ts, end_ts, time)
            
        return i_val
    

class Interpolator(object):
    """With this class, a sequence of TS_Unit objects can be represented
    
    >>> tsu1 = TS_Unit(ICollection.linear,
    ... Time_Period(datetime.datetime(2017, 07, 25, 20, 0, 0), datetime.datetime(2017, 07, 25, 20, 0, 10)))
    >>> tsu2 = TS_Unit(ICollection.constant,
    ... Time_Period(datetime.datetime(2017, 07, 25, 20, 0, 10), datetime.datetime(2017, 07, 25, 20, 0, 20)))
    >>> ip = Interpolator([tsu1, tsu2])
    """
    def __init__(self, ts_unit_list):
        """
        Args:
            ts_unit_list (list of sptemp.zeit.TS_Unit): List of TS_Unit objects. The end_time() of each TS_Unit object must be equal to
                the start_time() of the next TS_Unit object in the list. Thus there must be no gaps in time between the objects and no overlaps.
            
        Raises:
            ValueError: If empty list is passed or ts_unit_list is not correctly sorted
            TypeError: If ts_unit_list contains values that are not of type sptemp.zeit.TS_Unit
        """
        if not ts_unit_list:
            raise ValueError(text.IP_Texts.init_error1)
        
        elif isinstance(ts_unit_list, list) is False:
            raise TypeError(text.IP_Texts.init_error2)
        
        for i, tsu in enumerate(ts_unit_list):
            if isinstance(tsu, TS_Unit) is False:
                raise TypeError(text.IP_Texts.init_error2)
            
            elif i > 0 and ts_unit_list[i-1].ts.meets(tsu.ts) is False:
                raise ValueError(text.IP_Texts.init_error3)
            
        self._ts_unit_list = copy.deepcopy(ts_unit_list)
        
    def __len__(self):
        """
        Returns:
            int: Returns number of sptemp.zeit.TS_Unit objects stored in Interpolator
        """
        return len(self._ts_unit_list)
        
    def __getitem__(self, key):
        """
        Args:
            key (int or slice): the index
            
        Returns:
            sptemp.zeit.TS_Unit or list of sptemp.zeit.TS_Unit: returns indexed part of ts_unit_list
        """
        return copy.deepcopy(self._ts_unit_list[key])
    
    def __setitem__(self, key, value):
        """
        Args:
            key (int): the index
            value (sptemp.zeit.TS_Unit): new TS_Unit -> Must have same Time_Period as TS_Unit that it replaces 
            
        Raises:
            TypeError: If key is not of type integer or value is not of type sptemp.zeit.TS_Unit
            IndexError: If key is out of range
            ValueError: If value.ts is not equal to ts of TS_Unit that will be replaced
        """
        if isinstance(key, int) is False:
            raise TypeError(text.IP_Texts.set_error1)
        
        elif isinstance(value, TS_Unit) is False:
            raise TypeError(text.IP_Texts.set_error2)
        
        try:
            i_tu = self.__getitem__(key)
        except (IndexError):
            raise IndexError(text.IP_Texts.set_error3)
        
        if i_tu.ts != value.ts:
            raise ValueError(text.IP_Texts.set_error4)
        else:
            self._ts_unit_list[key] = copy.deepcopy(value)
            
    def __delitem__(self, key):
        """Deletes first or last item of the object
        
        Args:
            key (int): the index
            
        Raises:
            ValueError: If key is not 0 AND the key does not index the last item of the object
                OR if deletion would leave object beeing empty
        """
        if key != 0 and key != -1 and key != len(self._ts_unit_list)-1:
            raise ValueError(text.IP_Texts.del_error1)
        
        elif len(self._ts_unit_list) == 1:
            raise ValueError(text.IP_Texts.del_error2)
        
        else:
            del self._ts_unit_list[key]
            
    def interpolate(self, start_ts, end_ts, time, *args):
        """Interpolates value based on start_ts and end_ts at time instant 'time'
        
        >>> tsp1 = TS_Object(10.0, datetime.datetime(2017, 07, 25, 20, 0, 5))
        >>> tsp2 = TS_Object(20.0, datetime.datetime(2017, 07, 25, 20, 0, 15))
        >>> ip.interpolate(tsp1, tsp2, datetime.datetime(2017, 07, 25, 20, 0, 12))
        TS_Object(15.0, datetime.datetime(2017, 07, 25, 20, 0, 12))
        
        Args:
            start_ts (sptemp.zeit.TS_Object): previous TS_Object of 'time'
            end_ts (sptemp.zeit.TS_Object): next TS_Object of 'time'
            time (datetime.datetime): time for which value will be interpolated
            *args: arbitrary arguments that will be additionally passed to interpolation functions
        
        Returns:
            sptemp.zeit.TS_Object or NoneType: returns TS_Object with the value beeing the interpolated value
        
        Raises:
            TypeError: if type of start_ts or end_ts is not sptemp.zeit.TS_Object OR if type of time is not datetime.datetime
            ValueError: if start_ts.end_time() < self.start_time() OR time < start_ts.end_time() or time > end_ts.start_time()
                OR time < self.start_time() or time > self.end_time() OR start_ts.end_time() >= end_ts.end_time().
        """
        if isinstance(start_ts, TS_Object) is False or isinstance(end_ts, TS_Object) is False:
            raise TypeError(text.IP_Texts.ip_error1)
        
        elif isinstance(time, dt.datetime) is False:
            raise TypeError(text.IP_Texts.ip_error2)
        
        elif start_ts.end_time() < self.start_time():
            raise ValueError(text.IP_Texts.ip_error3)
        
        elif time < start_ts.end_time() or time > end_ts.start_time():
            raise ValueError(text.IP_Texts.ip_error4)
        
        elif time < self.start_time() or time > self.end_time():
            raise ValueError(text.IP_Texts.ip_error5)
        
        elif start_ts.end_time() >= end_ts.end_time():
            raise ValueError(text.IP_Texts.ip_error6)
        
        start_list = [tsu.start_time() for tsu in self._ts_unit_list]
        
        left = bisect.bisect_right(start_list, start_ts.end_time()) - 1
        right = bisect.bisect_left(start_list, time) - 1 if time != start_ts.end_time() else left
        
        r_unit = None
        sts = start_ts
        for i in range(left, right + 1):
            t = time if i == right else self._ts_unit_list[i].end_time()
            if args:
                r_unit = self._ts_unit_list[i].interpolate(sts, end_ts, t, *args)
            else:
                r_unit = self._ts_unit_list[i].interpolate(sts, end_ts, t)
            
            sts = r_unit
            
        return r_unit
        
    def value(self, time):
        """
        Args:
            time (datetime.datetime): Point in time for which value will be returned
            
        Returns:
            list of sptemp.zeit.TS_Unit: If 'time' is end_time of one Ts_Unit and start_time of another TS_Unit,
            the return list will contain two elements, else the list will contain one element. If time < self.start_time()
            or time > self.end_time(), the method will return an empty list.
                
        Raises:
            TypeError: if time is not of type datetime.datetime
        """
        if isinstance(time, dt.datetime) is False:
            raise TypeError(text.IP_Texts.val_error1)
        
        if time < self.start_time() or time > self.end_time():
            return []
        
        elif time == self.start_time():
            return [copy.deepcopy(self._ts_unit_list[0])]
        
        elif time == self.end_time():
            return [copy.deepcopy(self._ts_unit_list[-1])]
        
        start_list = [tsu.start_time() for tsu in self._ts_unit_list]
        
        left = bisect.bisect_left(start_list, time) - 1
        right = bisect.bisect_right(start_list, time) - 1
        
        if left == right:
            return [copy.deepcopy(self._ts_unit_list[left])]
        else:
            return [copy.deepcopy(self._ts_unit_list[left]), copy.deepcopy(self._ts_unit_list[right])]
        
    def slice(self, time):
        """
        Args:
            time (sptemp.zeit.Time_Period): Time_Period for which slice will be created
            
        Returns:
            sptemp.zeit.Interpolator or NoneType: Returns time-slice of original Interpolator,
            returns None if slice of Interpolator is empty
            
        Raises:
            TypeError: if type(time) != sptemp.zeit.Time_Period
        """
        if isinstance(time, Time_Period) is False:
            raise TypeError(text.IP_Texts.slice_error1)
        
        tp = Time_Period(self.start_time(), self.end_time())
        if tp.contains(time.start) is False and tp.contains(time.end) is False:
            return None
        
        start_list = [tsu.start_time() for tsu in self._ts_unit_list]
        
        left = bisect.bisect_right(start_list, time.start) - 1 if time.start >= self.start_time() else 0
        right = bisect.bisect_left(start_list, time.end) - 1
        
        # time adjustment of first and last TS_Unit 
        r_list = self._ts_unit_list[left:(right + 1)]
        if r_list[0].start_time() <= time.start:
            tsu_start = TS_Unit(r_list[0].value, Time_Period(time.start, r_list[0].end_time()))
            del r_list[0]
            r_list.insert(0, tsu_start)
        
        if r_list[-1].end_time() >= time.end:
            tsu_end = TS_Unit(r_list[-1].value, Time_Period(r_list[-1].start_time(), time.end))
            del r_list[-1]
            r_list.append(tsu_end)
            
        return Interpolator(r_list)
        
    def as_list(self):
        """
        Returns:
            list of sptemp.zeit.TS_Unit: returns copy of ts_unit_list stored in Interpolator object
        """
        return copy.deepcopy(self._ts_unit_list)
    
    def start_time(self):
        """
        Returns:
            datetime.datetime: Returns start_time of first element of the ts_unit_list of the object
        """
        return copy.deepcopy(self._ts_unit_list[0].start_time())
    
    def end_time(self):
        """
        Returns:
            datetime.datetime: Returns end_time of last element of the ts_unit_list of the object
        """
        return copy.deepcopy(self._ts_unit_list[-1].end_time())
    
    def i_unit(self, i):
        """
        Args:
            i (int): index for Interpolator
            
        Returns:
            returns TS_Unit at position i in Interpolator sequence (Interpolator[i])
        """
        return copy.deepcopy(self._ts_unit_list[i])
    
    def append(self, value):
        """
        Args:
            value (sptemp.zeit.TS_Unit): TS_Unit Object that will be appended to Interpolator
        
        Raises:
            TypeError: If value is not of type sptemp.zeit.TS_Unit
            ValueError: If value.start_time() != Interpolator.end_time()
        """
        if isinstance(value, TS_Unit) is False:
            raise TypeError(text.IP_Texts.app_error1)
        
        elif value.start_time() != self.end_time():
            raise ValueError(text.IP_Texts.app_error2)
        
        else:
            self._ts_unit_list.append(copy.deepcopy(value))
            
    def insert(self, value):
        """Insert TS_Unit object into Interpolator
        
        Note:
            Existing values will be overwritten or ajusted
            
        Args:
            value (sptemp.zeit.TS_Unit): TS_Unit that will be inserted into Interpolator
        
        Raises:
            TypeError: If value is not of type sptemp.zeit.TS_Unit
            ValueError: If value.ts lays outside existing time-coverage of Interpolator
        """
        if isinstance(value, TS_Unit) is False:
            raise TypeError(text.IP_Texts.in_error1)
        
        tp = Time_Period(self.start_time(), self.end_time())
        if tp.includes(value.start_time()) is False and tp.includes(value.end_time()) is False:
            if (value.start_time() < self.start_time() and value.end_time() > self.end_time()) is False:
                raise ValueError(text.IP_Texts.in_error2)
        
        if value.end_time() == self.start_time():
            self._ts_unit_list.insert(0, copy.deepcopy(value))
            return
            
        elif value.start_time() == self.end_time():
            self.append(copy.deepcopy(value))
            return
        
        start_list = [tsu.start_time() for tsu in self._ts_unit_list]
        end_list = [tsu.end_time() for tsu in self._ts_unit_list]
        
        start_i = bisect.bisect_right(start_list, value.start_time()) - 1 if value.start_time() >= start_list[0] else 0
        end_i = bisect.bisect_left(start_list, value.end_time()) - 1 if value.end_time() <= end_list[-1] else self.__len__() - 1
        
        start_unit = self._ts_unit_list[start_i]
        end_unit = self._ts_unit_list[end_i]
        
        if start_i == end_i:
            # replace existing TS_Unit
            if start_unit.start_time() == value.start_time() and end_unit.end_time() == value.end_time():
                self._ts_unit_list[start_i] = copy.deepcopy(value)
                return
                
            # split existing TS_Unit
            elif start_unit.ts.contains(value.ts):
                left = TS_Unit(start_unit.value, Time_Period(start_unit.start_time(), value.start_time()))
                # middle = value
                right = TS_Unit(start_unit.value, Time_Period(value.end_time(), end_unit.end_time()))
                
                del self._ts_unit_list[start_i]
                self._ts_unit_list.insert(start_i, left)
                self._ts_unit_list.insert(start_i + 1, copy.deepcopy(value))
                self._ts_unit_list.insert(start_i + 2, right)
                return
            
            # adjust existing TS_Unit on the left
            elif start_unit.start_time() >= value.start_time() and end_unit.end_time() > value.end_time():
                right = TS_Unit(start_unit.value, Time_Period(value.end_time(), end_unit.end_time()))
                del self._ts_unit_list[end_i]
                self._ts_unit_list.insert(start_i, copy.deepcopy(value))
                self._ts_unit_list.insert(start_i + 1, right)
                return
            
            # adjust existing TS_Unit on the right
            elif start_unit.start_time() < value.start_time() and end_unit.end_time() <= value.end_time():
                left = TS_Unit(start_unit.value, Time_Period(start_unit.start_time(), value.start_time()))
                del self._ts_unit_list[start_i]
                self._ts_unit_list.insert(start_i, left)
                self._ts_unit_list.insert(start_i + 1, copy.deepcopy(value))
        
        else:
            # no adjusting of ts of existing TS_Units needed
            if value.start_time() <= start_unit.start_time() and value.end_time() >= end_unit.end_time():
                del self._ts_unit_list[start_i:end_i + 1]
                self._ts_unit_list.insert(start_i, copy.deepcopy(value))
                return
            # adjustment of existing TS_Units
            else:
                if value.start_time() > start_unit.start_time():
                    left = TS_Unit(start_unit.value, Time_Period(start_unit.start_time(), value.start_time()))
                else:
                    left = None
                
                if value.end_time() < end_unit.end_time():
                    right = TS_Unit(end_unit.value, Time_Period(value.end_time(), end_unit.end_time()))
                else:
                    right = None
                    
                if left:
                    del self._ts_unit_list[start_i]
                    self._ts_unit_list.insert(start_i, left)
                    start_i += 1
                    del self._ts_unit_list[end_i]
                    if right:
                        self._ts_unit_list.insert(end_i, right)
                    self._ts_unit_list.insert(start_i, copy.deepcopy(value))
                
                else:
                    del self._ts_unit_list[start_i]
                    self._ts_unit_list.insert(start_i, copy.deepcopy(value))
                    del self._ts_unit_list[end_i]
                    if right:
                        self._ts_unit_list.insert(end_i, right)
                
                delete_list = []
                for i in range(start_i + 1, self.__len__()):
                    if self._ts_unit_list[i].start_time() != value.end_time():
                        delete_list.append(i)
                        
                for _ in delete_list:
                    del self._ts_unit_list[delete_list[0]]
                    
    def delete(self, time):
        """Deletes TS_unit elements from Interpolator
        
        Args:
            time (sptemp.zeit.Time_Period): Time Period that will be deleted from Interpolator
            
        Raises:
            TypeError: If time is not of type sptemp.zeit.Time_Period
            ValueError: If Time_Period covers the whole timespan of the Interpolator -> Deletion would leave Interpolator empty 
                OR if ime is contained by the timespan of the Interpolator and thus the deletion would create a gap
        """
        if isinstance(time, Time_Period) is False:
            raise TypeError(text.IP_Texts.delete_error1)
        
        elif time.start <= self.start_time() and time.end >= self.end_time():
            raise ValueError(text.IP_Texts.delete_error2)
        
        tp = Time_Period(self.start_time(), self.end_time())
        if tp.contains(time.start) and tp.contains(time.end):
            raise ValueError(text.IP_Texts.delete_error3)
        
        # nothing is deleted
        if tp.contains(time.start) is False and tp.contains(time.end) is False:
            return
        
        start_list = [tsu.start_time() for tsu in self._ts_unit_list]
        
        if time.end < self.end_time():
            end_i = bisect.bisect_left(start_list, time.end) - 1
            del self._ts_unit_list[:end_i]
            if self._ts_unit_list[0].end_time() == time.end:
                del self._ts_unit_list[0]
            else:
                right = TS_Unit(self._ts_unit_list[0].value, Time_Period(time.end, self._ts_unit_list[0].end_time()))
                del self._ts_unit_list[0]
                self._ts_unit_list.insert(0, right)
                
        else:
            start_i = bisect.bisect_right(start_list, time.start) - 1
            del self._ts_unit_list[(start_i + 1):]
            if self._ts_unit_list[-1].start_time() == time.start:
                del self._ts_unit_list[-1]
            else:
                left = TS_Unit(self._ts_unit_list[-1].value, Time_Period(self._ts_unit_list[-1].start_time(), time.start))
                del self._ts_unit_list[-1]
                self.append(left)
                
    def length(self):
        """
        Returns:
            int: Returns number of sptemp.zeit.TS_Unit objects stored in Interpolator
        """
        return len(self._ts_unit_list)
            
        
class Moving_Object(object):
    """With this class a sequence of disjoint TS_Objects can be represented
    
    >>> tsu1 = TS_Unit(ICollection.linear,
    ... Time_Period(datetime.datetime(2017, 07, 25, 20, 0, 0), datetime.datetime(2017, 07, 25, 20, 0, 10)))
    >>> tsu2 = TS_Unit(ICollection.constant,
    ... Time_Period(datetime.datetime(2017, 07, 25, 20, 0, 10), datetime.datetime(2017, 07, 25, 20, 0, 20)))
    >>> ip = Interpolator([tsu1, tsu2])
    >>> tsp1 = TS_Object(10.0, datetime.datetime(2017, 07, 25, 20, 0, 5))
    >>> tsp2 = TS_Object(20.0, datetime.datetime(2017, 07, 25, 20, 0, 15))
    >>> mo1 = Moving_Object([tsp1, tsp2], ip)
    
    Attributes:
        interpolator (sptemp.zeit.Interpolator): Interpolator associated with the Moving_Object
    """
    def __init__(self, ts_object_list, interpolator):
        """
        Args:
            ts_object_list (list of sptemp.zeit.TS_Object): time-sorted list of disjoint TS_Object instances
            interpolator (sptemp.zeit.Interpolator): Interpolator object that will be used to interpolate values of the Moving_Object
            
        Raises:
            TypeError: if ts_object_list is not of type list OR if ts_object_list contains objects that are nor of type sptemp.zeit.TS_Object
                OR interpolator is not of type sptemp.zeit.Interpolator
            ValueError: if len(ts_object_list) == 0 OR TS_Objects do not all have the same type OR if timestamps of TS_Objects are not disjoint
        """
        if not ts_object_list:
            raise ValueError(text.MO_Texts.init_error1)
        
        elif isinstance(ts_object_list, list) is False:
            raise TypeError(text.MO_Texts.init_error2)
        
        elif isinstance(interpolator, Interpolator) is False:
            raise TypeError(text.MO_Texts.init_error3)
        
        for i, tso in enumerate(ts_object_list):
            if isinstance(tso, TS_Object) is False:
                raise TypeError(text.MO_Texts.init_error2)
            
            elif i > 0 and tso.type != ts_object_list[0].type:
                raise TypeError(text.MO_Texts.init_error4)
            
            elif (i > 0) and (tso.start_time() <= ts_object_list[i-1].end_time()):
                raise ValueError(text.MO_Texts.init_error5)
            
        self._ts_object_list = copy.deepcopy(ts_object_list)
        self._type = self._ts_object_list[0].type
        self.interpolator = interpolator
        
    @property
    def type(self):
        return self._type
    
    def __len__(self):
        """
        Returns:
            int: Returns number of sptemp.zeit.TS_Object instances stored in Moving_Object
        """
        return len(self._ts_object_list)
        
    def __getitem__(self, key):
        """
        Args:
            key (int or slice): the index
            
        Returns:
            sptemp.zeit.TS_Object or list of sptemp.zeit.TS_Object: returns indexed part of ts_object_list
        """
        return copy.deepcopy(self._ts_object_list[key])
    
    def __setitem__(self, key, value):
        """
        Args:
            key (int): the index
            value (sptemp.zeit.TS_Object): new TS_Object
            
        Raises:
            TypeError: If key is not of type integer, if value is not of type sptemp.zeit.TS_Object
            IndexError: If key is out of range
            ValueError: If value.ts is not disjoint to existing Ts_Objects in Moving_Object or value.type != self.type
        """
        if isinstance(key, int) is False:
            raise TypeError(text.MO_Texts.set_error1)
        
        elif isinstance(value, TS_Object) is False:
            raise TypeError(text.MO_Texts.set_error2)
        
        elif self.type != value.type:
            raise ValueError(text.MO_Texts.set_error3)
        
        try:
            tso_x = self.__getitem__(key)
        except (IndexError):
            raise IndexError(text.MO_Texts.set_error4)
        
        # if key does not index first item of moving_object
        if tso_x != self.__getitem__(0):
            if value.start_time() <= self._ts_object_list[key-1].end_time():
                raise ValueError(text.MO_Texts.set_error5)
        
        # if key does not index last item of moving_object    
        if tso_x != self.__getitem__(-1):
            if value.end_time() >= self._ts_object_list[key+1].start_time():
                raise ValueError(text.MO_Texts.set_error5)
            
        self._ts_object_list[key] = copy.deepcopy(value)
        
    def __delitem__(self, key):
        """
        Args:
            key (int or slice): index of TS_Objects that will be deleted
        
        Raises:
            TyperError: if key is not of type int or slice
            ValueError: if deletion would leave Moving_Object empty
        """ 
        if isinstance(key, int) is False and isinstance(key, slice) is False:
            raise TypeError(text.MO_Texts.del_error1)
        
        elif self.__len__() == 1:
            raise ValueError(text.MO_Texts.del_error2)
        
        if isinstance(key, int):
            del self._ts_object_list[key]
            
        else:
            s_start = key.start if key.start is not None else 0
            s_stop = key.stop if key.stop is not None else self.__len__()
            s_step = key.step if key.step is not None else 1
            len_slice = abs(s_stop - s_start)
            if len_slice >= self.__len__() and s_step == 1:
                raise ValueError(text.MO_Texts.del_error2)
            else:
                del self._ts_object_list[key]
                
    def interpolate(self, time, *args):
        """
        Args:
            time (datetime.datetime): point in time for which value of Moving_Object will be returned
            *args: arbitrary arguments that will be passed to Interpolator
            
        Returns:
            sptemp.zeit.TS_Object or NoneType: If 'time' is included in the timestamps than than a TS_Object is returned with the corresponding value,
            and the 'time' as timestamp. If 'time' lays between the TS_Objects, than the associated Interpolator is used,
            to interpolate the value at this point in time.
            Returns None if time < self.start_time() or time > self.end_time() or interpolation function returned None
        
        Raises:
            TypeError: if type time is not datetime.datetime.
            ValueError: if TS_Object.type returned by Interpolator != self.type
        """
        if isinstance(time, dt.datetime) is False:
            raise TypeError(text.MO_Texts.i_error1)
        
        elif time < self.start_time() or time > self.end_time():
            return None
        
        left = self.prev_i(time)
        right = self.next_i(time)
        
        l_tso = self.__getitem__(left)
        r_tso = self.__getitem__(right)
        
        if l_tso.ts == time or left == right:
            return l_tso.__class__(l_tso.value, time) if hasattr(l_tso, "crs") is False else l_tso.__class__(l_tso.value, time, l_tso.crs)
        else:
            tso = self.interpolator.interpolate(l_tso, r_tso, time, *args)
            if tso is None or tso.value is None:
                return None
            
            elif tso.type != self.type:
                raise ValueError(text.MO_Texts.i_error3)
            
            else:
                return tso
        
    def slice(self, time):
        """
        Args:
            time (sptemp.zeit.Time_Period): Time_Period for which slice will be created
            
        Returns:
            sptemp.zeit.Moving_Object or NoneType: Returns time-slice of original Moving_Object, returns None if slice is empty
            
        Raises:
            TypeError: if type(time) != sptemp.zeit.Time_Period
        """
        if isinstance(time, Time_Period) is False:
            raise TypeError(text.MO_Texts.slice_error1)
        
        elif time.end < self.start_time() or time.start > self.end_time():
            return None
        
        left = self.prev_i(time.start) if self.prev_i(time.start) is not None else 0
        right = self.next_i(time.end) if self.next_i(time.end) is not None else self.__len__()
        
        r_list = self.__getitem__(slice(left, right + 1)) if left != right else [self.__getitem__(left)]
        
        if time.start > r_list[0].end_time():
            del r_list[0]
            
        elif time.start == r_list[0].end_time() and isinstance(r_list[0].ts, Time_Period):
            new_l_tso = TS_Object(r_list[0].value, r_list[0].end_time())
            del r_list[0]
            r_list.insert(0, new_l_tso)
            
        elif time.end == r_list[0].start_time() and isinstance(r_list[0].ts, Time_Period):
            new_l_tso = TS_Object(r_list[0].value, r_list[0].start_time())
            del r_list[0]
            r_list.insert(0, new_l_tso)
            
        elif time.start > r_list[0].start_time() and time.start < r_list[0].end_time():
            new_l_tso = TS_Object(r_list[0].value, Time_Period(time.start, r_list[0].end_time()))
            del r_list[0]
            r_list.insert(0, new_l_tso)
            
        if len(r_list) == 0:
            return None
        
        else:
            if time.end < r_list[-1].start_time():
                del r_list[-1]
                
            elif time.end == r_list[-1].start_time() and isinstance(r_list[-1].ts, Time_Period):
                new_r_tso = TS_Object(r_list[-1].value, r_list[-1].start_time())
                del r_list[-1]
                r_list.append(new_r_tso)
                
            elif time.start == r_list[-1].end_time() and isinstance(r_list[-1].ts, Time_Period):
                new_r_tso = TS_Object(r_list[-1].value, r_list[-1].end_time())
                del r_list[-1]
                r_list.append(new_r_tso)
                
            elif time.end < r_list[-1].end_time() and time.end > r_list[-1].start_time():
                new_r_tso = TS_Object(r_list[-1].value, Time_Period(r_list[-1].start_time(), time.end))
                del r_list[-1]
                r_list.append(new_r_tso)
                
        if len(r_list) == 0:
            return None
        else:
            return self.__class__(r_list, self.interpolator)
        
    def resampled_slice(self, times, time_args=None):
        """
        Returns slice between first time instant of times and last time instant of times.
        If Moving_Object is not defined at time instants in 'times', the interpolator is used,
        and a TS_Object is inserted into the slice.
        
        Args:
            times (list of datetime.datetime): List of time instants
            time_args (sptemp.zeit.Moving_Object, optional): Moving_Object, which holds timestamped lists,
                that define which args are passed to Interpolator, at which points in time.
            
        Returns:
            sptemp.zeit.Moving_Object or NoneType: Returns resampled-slice of original Moving_Object.
            Returns None if slice is empty
            
        Raises:
            TypeError: if type of times is not list
            ValueError: if len(times) < 2
        """
        if isinstance(times, list) is False:
            raise TypeError(text.MO_Texts.re_slice_error1)
        
        if len(times) < 2:
            raise ValueError(text.MO_Texts.re_slice_error2)
        
        elif times[-1] < self.start_time() or times[0] > self.end_time():
            return None
        
        t_slice = self.slice(Time_Period(times[0], times[-1]))
        
        ts_list = []  
        
        for t in times:
            arg = time_args.interpolate(t).value if time_args and time_args.interpolate(t) else None
            ip_ts = self.interpolate(t, *arg) if arg else self.interpolate(t)
            
            if t_slice is None:
                if ip_ts is not None:
                    ts_list.append(ip_ts)
                
            else:
                try:
                    if ip_ts is not None:
                        t_slice.insert(ip_ts)
                except ValueError:
                    pass
        
        if t_slice is None and ts_list:
            return self.__class__(ts_list, self.interpolator)
        else:
            return t_slice
                
    def as_list(self):
        """
        Returns:
            list of sptemp.zeit.TS_Object: returns copy of ts_object_list stored in Moving_Object
        """
        return copy.deepcopy(self._ts_object_list)
    
    def i_object(self, i):
        """
        Args:
            i (int): index for Moving_Object
            
        Returns:
            returns TS_Object at position i in Moving_Object sequence (Moving_Object[i])
        """
        return copy.deepcopy(self._ts_object_list[i])
    
    def prev_i(self, time):
        """
        Args:
            time (datetime.datetime): time for which index of previous TS_Object will be returned.
        
        Returns:
            int or None: returns index of TS_Object that lays directly before time. If time is equal to a
            ts of a TS_object or is inlcuded in the ts of a Ts_Object, than index of this TS_Object is returned. 
            Returns None, if time < self.start_time().
        """
        if isinstance(time, dt.datetime) is False:
            raise TypeError(text.MO_Texts.prev_error1)
        
        if time < self.start_time():
            return None
        
        start_list = [tso.start_time() for tso in self._ts_object_list]
        prev = bisect.bisect_right(start_list, time) - 1
        
        return prev
    
    def next_i(self, time):
        """
        Args:
            time (datetime.datetime): time for which index of next TS_Object will be returned.
        
        Returns:
            int or None: returns index of TS_Object that lays directly after time. If time is equal to a
            ts of a TS_object or is inlcuded in the ts of a Ts_Object, than index of this TS_Object is returned. 
            Returns None, if time > self.end_time().
        """
        if isinstance(time, dt.datetime) is False:
            raise TypeError(text.MO_Texts.prev_error1)
        
        if time > self.end_time():
            return None
        
        end_list = [tso.end_time() for tso in self._ts_object_list]
        nx = bisect.bisect_left(end_list, time)
        
        return nx
    
    def start_time(self):
        """
        Returns:
            datetime.datetime: Returns start_time of first element of the ts_unit_list of the Moving_Object
        """
        return copy.deepcopy(self._ts_object_list[0].start_time())
    
    def end_time(self):
        """
        Returns:
            datetime.datetime: Returns end_time of last element of the ts_unit_list of the Moving_Object
        """
        return copy.deepcopy(self._ts_object_list[-1].end_time())
    
    def append(self, value):
        """
        Args:
            value (sptemp.zeit.TS_Object): TS_Object that will be appended to Moving_Object
        
        Raises:
            TypeError: If value is not of type sptemp.zeit.TS_Object
            ValueError: If value.start_time() <= Moving_Object.end_time()
        """
        if isinstance(value, TS_Object) is False:
            raise TypeError(text.MO_Texts.app_error1)
        
        elif value.start_time() <= self.end_time():
            raise ValueError(text.MO_Texts.app_error2)
        
        else:
            self._ts_object_list.append(copy.deepcopy(value))
            
    def insert(self, value):
        """Insert value into Moving_Object
        
        Note:
            In contrary to Interpolator objects -> Values will not be overwritten or adjusted
            
        Args:
            value (sptemp.zeit.TS_Object): TS_Object that will be inserted into Moving_Object
        
        Raises:
            TypeError: If value is not of type sptemp.zeit.TS_Object
            ValueError: If value.ts and timestamps of Ts_Objects in Moving Object are not disjoint
                or if value.type != self.type
        """
        if isinstance(value, TS_Object) is False:
            raise TypeError(text.MO_Texts.in_error1)
        
        elif self.type != value.type:
            raise ValueError(text.MO_Texts.in_error3)
        
        left = self.prev_i(value.start_time())
        right = self.next_i(value.start_time())
        
        # value lays before first value of Moving_Object
        if left is None and right is 0 and value.end_time() < self.start_time():
            self._ts_object_list.insert(0, copy.deepcopy(value))
            
        # value lays after last value of Moving_Object
        elif right is None and left == (self.__len__() - 1) and value.start_time() > self.end_time():
            self.append(copy.deepcopy(value))
            
        elif right is None or left is None:
            raise ValueError(text.MO_Texts.in_error2)
            
        elif (right - left == 1) and value.start_time() > self.__getitem__(left).end_time() and value.end_time() < self.__getitem__(right).start_time():
            self._ts_object_list.insert(right, copy.deepcopy(value))
            
        else:
            raise ValueError(text.MO_Texts.in_error2)
        
    def delete(self, time):
        """Deletes TS_Objects from Moving_Object.
        All TS_Object of which the timestamps are contained in the Time_Period are deleted, overlapping timestamps are adjusted.
        If ts of TS_Object is adjusted -> TS_Object.end_time() == time.start or TS_Object.start_time() == time.end
        IF type(time) == datetime.datetime, TS_Object is only deleted if TS_Object.ts == time.
        
        Args:
            time (datetime.datetime or sptemp.zeit.Time_Period): Time that will be deleted from Moving Object
                        
        Raises:
            TypeError: If time is not of type sptemp.zeit.Time_Period
            ValueError: If Time_Period covers the whole timespan of the Moving_Object -> Deletion would leave Moving_Object empty 
        """
        if isinstance(time, Time_Period) is False:
            raise TypeError(text.MO_Texts.delete_error1)
        
        elif time.start < self.start_time() and time.end > self.end_time():
            raise ValueError(text.MO_Texts.delete_error2)
                
        else:
            # if time outside timespan of Moving_Object -> nothing is deleted
            if time.end < self.start_time() or time.start > self.end_time():
                return
            
            left = self.prev_i(time.start) if self.prev_i(time.start) is not None else 0
            right = self.next_i(time.end) if self.next_i(time.end) is not None else self.__len__() - 1
            
            l_tso = self.__getitem__(left)
            r_tso = self.__getitem__(right)
            
            # if time is contained in ts of TS_Object -> TS_Object is split
            if left == right:
                if time.start == l_tso.start_time():
                    new_l_tso = TS_Object(l_tso.value, l_tso.start_time())
                    self.__delitem__(left)
                    self.insert(new_l_tso)
                    right += 1
                    
                elif time.start > l_tso.start_time():
                    new_l_tso = TS_Object(l_tso.value, Time_Period(l_tso.start_time(), time.start))
                    self.__delitem__(left)
                    self.insert(new_l_tso)
                    right += 1
                    
                if time.end == r_tso.end_time():
                    new_r_tso = TS_Object(r_tso.value, r_tso.end_time())
                    if left == right:
                        self.__delitem__(right)
                    self.insert(new_r_tso)
                    
                elif time.end < r_tso.end_time():
                    new_r_tso = TS_Object(r_tso.value, Time_Period(time.end, r_tso.end_time()))
                    if left == right:
                        self.__delitem__(right)
                    self.insert(new_r_tso)
                    
            else:
                if time.start == l_tso.start_time() and isinstance(l_tso.ts, Time_Period):
                    new_l_tso = TS_Object(l_tso.value, l_tso.start_time())
                    self.__delitem__(left)
                    self.insert(new_l_tso)
                    
                elif time.start > l_tso.start_time() and time.start < l_tso.end_time():
                    new_l_tso = TS_Object(l_tso.value, Time_Period(l_tso.start_time(), time.start))
                    self.__delitem__(left)
                    self.insert(new_l_tso)
                    
                if time.end == r_tso.end_time() and isinstance(r_tso.ts, Time_Period):
                    new_r_tso = TS_Object(r_tso.value, r_tso.end_time())
                    self.__delitem__(right)
                    self.insert(new_r_tso)
                    
                elif time.end < r_tso.end_time() and time.end > r_tso.start_time():
                    new_r_tso = TS_Object(r_tso.value, Time_Period(time.end, r_tso.end_time()))
                    self.__delitem__(right)
                    self.insert(new_r_tso)
                
                if time.start >= self.start_time():
                    left += 1
                    
                # delete TS_objects in between left and right
                while True:
                    if left == self.__len__():
                        break
                    
                    elif self.__getitem__(left).start_time() < time.end:
                        self.__delitem__(left)
                        
                    else:
                        break
                    
    def length(self):
        """
        Returns:
            int: Returns number of sptemp.zeit.TS_Object instances stored in Moving_Object
        """
        return len(self._ts_object_list)
                    

class ZeitHelper:
    
    @staticmethod
    def parse_time_from_iso(time):
        """
        Args:
            time (string): time_instant in the iso8601 format
            
        Returns:
            datetime.datetime: returns time as datetime.datetime object
        """
        from dateutil import parser
        
        return parser.parse(time)
    
