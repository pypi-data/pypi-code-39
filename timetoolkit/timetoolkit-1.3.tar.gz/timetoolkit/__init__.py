# !usr\bin\env python
# -*- coding:utf-8 -*-

"""
Some great tools about time.

Functions:

    Compile(x, y) -> bool
    FormatTimeNow(format_str='%Y-%m-%d %H:%M:%S') -> str
    FormatTimeTuple(p_tuple=None) -> str
    FormatTimeStamp(time_stamp=None) -> str
    FormatDateTime(DateTime=None) -> str
    ParseInt(timeunitobj) -> int
    ParseFloat(timeunitobj) -> float
    ParseList(DateTimeobj) -> list
    ParseDict(timetableobj) -> dict
    GetTimeNow() -> str
    GetCalendarThisYear() -> Calendar
    GetCalendarByYear(year) -> Calendar
    GetStructTimeNow() -> time.struct_time
    GetDateTimeNow() -> DateTime
    GetDateNow() -> Date
    GetYearNow() -> Year
    GetMonthNow() -> Month
    GetDayNow() -> Day
    GetHourNow() -> Hour
    GetMinuteNow() -> Minute
    GetSecondNow() -> Second
    GetTimeStampNow() -> TimeStamp
    GetDatesIterator(year, month) -> generator
    IsLeapYearNow() -> bool
    RandomDateTime() -> DateTime
    RandomYear() -> Year
    RandomMonth() -> Month
    RandomDay() -> Day
    RandomHour() -> Hour
    RandomMinute() -> Minute
    RandomSecond() -> Second
    OutputCalendarThisYear() -> str
    DaysBeforeYear(year) -> Day
    DayInMonth(year, month) -> Day
    DaysBeforeMonth(year, month) -> Day

Classes:

    DateTime
    
        Methods:
        __init__(year=0,
                 month=0,
                 day=0,
                 hour=0,
                 minute=0,
                 second=0,
                 zero_point_one_second=0,
                 zero_point_zero_one_second=0,
                 zero_point_zero_zero_one_second=0) -> DateTime
        __add__(other) -> DateTime
        __iadd__(other) -> DateTime
        __len__() -> int
        __lt__(other) -> bool
        __ne__(other) -> bool
        __ge__(other) -> bool
        __gt__(other) -> bool
        __le__(other) -> bool
        __eq__(other) -> bool
        __iter__() -> list_iterator
        __next__() -> object
        __contains__(item) -> bool
        __getitem__(item) -> int
        __str__() -> str
        __repr__() -> str
        __bool__() -> True
        __format__(format_spec) -> str
        Clone() -> DateTime
        AutoGeneration() -> DateTime
        SetYear(year)
        SetMonth(month)
        SetDay(day)
        SetHour(hour)
        SetMinute(minute)
        SetSecond(second)
        SetZeroPointOneSecond(zero_point_one_second)
        SetZeroPointZeroOneSecond(zero_point_zero_one_second)
        SetZeroPointZeroZeroOneSecond(zero_point_zero_zero_one_second)
        GetYear() -> int
        GetMonth() -> int
        GetDay() -> int
        GetHour() -> int
        GetMinute() -> int
        GetSecond() -> int
        GetZeroPointOneSecond() -> int
        GetZeroPointZeroOneSecond() -> int
        GetZeroPointZeroZeroOneSecond() -> int
        Transform(unit) -> float
        Difference() -> DateTime
        Format(format_spec) -> str
        GetWeekDay() -> int (range[1, 7], Monday is 0)
        ToTimeStamp() -> TimeStamp
        Add(other) -> DateTime
        IsLeapYear() -> bool
        GetList() -> list
        GetYearDay() -> int (range[1, 366])

        Properties:
            time_list
            year
            month
            day
            hour
            minute
            second
            zero_point_one_second
            zero_point_zero_one_second
            zero_point_zero_zero_one_second
            _list (protected)
            __len (private)

    TimeTable
    
        Methods:
        __init__(time_table_dict) -> TimeTable
        __str__() -> str
        __repr__() -> str
        __bool__() -> bool
        __contains__(item) -> bool
        __len__() -> int
        __reversed__() -> TimeTable
        Add(time, action)
        AddMany(time_table_dict)
        Clone() -> TimeTable
        Remove(time)
        RemoveMany(*times)
        Get(time, default='') -> str
        GetMany(*times, default="") -> str
        GetTimes() -> list
        GetActions() -> list
        Clear()
        Set(time, action, default_action='')
        IsEmpty() -> bool
        CreateFile(table_name, location)
        OpenFile(file) -> TimeTable
        CheckExpire(time) -> bool
        Items() -> list
        Reverse() -> TimeTable

        Properties:
            dict
            _dict (provided)

    Timer
    
        Methods:
        __str__() -> str
        __add__(other) -> list
        __repr__() -> DateTime
        __lt__(other) -> bool
        __ne__(other) -> bool
        __ge__(other) -> bool
        __gt__(other) -> bool
        __le__(other) -> bool
        __eq__(other) -> bool
        Start()
        Stop()
        IsRunning() -> bool
        GetTime() -> DateTime
    
        Properties:
            running
            ___time (private)
            _time_list (provided)
            is_start
            is_stop
            ratio
            time
            timer_start
            timer_stop

    TimeUnit

        Methods:
            __init__(num=0) -> TimeUnit
            __str__() -> str
            __repr__() -> str
            __bool__() -> bool
            __add__(other) -> TimeUnit
            __iadd__(other) -> TimeUnit
            __sub__(other) -> TimeUnit
            __isub__(other) -> TimeUnit
            __mul__(other) -> TimeUnit
            __imul__(other) -> TimeUnit
            __gt__(other) -> bool
            __ge__(other) -> bool
            __lt__(other) -> bool
            __le__(other) -> bool
            __eq__(other) -> bool
            __ne__(other) -> bool
            __call__(num)
            __int__() -> int
            __float__() -> float
            __pos__() -> float or int
            __neg__() -> float or int
            __ceil__() -> int
            __floor__() -> int
            __trunc__() -> int

        Properties:
            _num
            _ratio

    Year(TimeUnit)

        Methods:
            __init__(num=0) -> Year
            __str__() -> str
            __repr__() -> str
            __bool__() -> bool
            __add__(other) -> TimeUnit
            __iadd__(other) -> TimeUnit
            __sub__(other) -> TimeUnit
            __isub__(other) -> TimeUnit
            __mul__(other) -> TimeUnit
            __imul__(other) -> TimeUnit
            __gt__(other) -> bool
            __ge__(other) -> bool
            __lt__(other) -> bool
            __le__(other) -> bool
            __eq__(other) -> bool
            __ne__(other) -> bool
            __call__(num)
            __int__() -> int
            __float__() -> float
            __pos__() -> float or int
            __neg__() -> float or int
            __ceil__() -> int
            __floor__() -> int
            __trunc__() -> int
            SetYear(year)
            GetYear() -> float or int
            TransformToMonth() -> Month
            TransformToDay() -> Day
            TransformToHour() -> Hour
            TransformToMinute() -> Minute
            TransformToSecond() -> Second
            AddTime(other) -> Year
            SubTime(other) -> Year
            MulTime(other) -> Year

        Properties:
            year
            _num (protected)
            _ratio (protected)

    Month(TimeUnit)

        Methods:
            __init__(month) -> Month
            __str__() -> str
            __repr__() -> str
            __bool__() -> bool
            __add__(other) -> Month
            __iadd__(other) -> Month
            __sub__(other) -> Month
            __isub__(other) -> Month
            __mul__(other) -> Month
            __imul__(other) -> Month
            __gt__(other) -> bool
            __ge__(other) -> bool
            __lt__(other) -> bool
            __le__(other) -> bool
            __eq__(other) -> bool
            __ne__(other) -> bool
            __call__(num)
            __int__() -> int
            __float__() -> float
            __pos__() -> float or int
            __neg__() -> float or int
            __ceil__() -> int
            __floor__() -> int
            __trunc__() -> int
            GetMonth() -> float or int
            SetMonth(month)
            TransformToYear() -> Year
            TransformToDay() -> Day
            TransformToHour() -> Hour
            TransformToMinute() -> Minute
            TransformToSecond() -> Second
            AddTime(other) -> Month
            SubTime(other) -> Month
            MulTime(other) -> Month

        Properties:
            month
            _num (protected)
            _ratio (protected)

    Day(TimeUnit)

        Methods:
            __init__(day) -> Day
            __str__() -> str
            __repr__() -> str
            __bool__() -> bool
            __add__(other) -> Day
            __iadd__(other) -> Day
            __sub__(other) -> Day
            __isub__(other) -> Day
            __mul__(other) -> Day
            __imul__(other) -> Day
            __gt__(other) -> bool
            __ge__(other) -> bool
            __lt__(other) -> bool
            __le__(other) -> bool
            __eq__(other) -> bool
            __ne__(other) -> bool
            __call__(num)
            __int__() -> int
            __float__() -> float
            __pos__() -> float or int
            __neg__() -> float or int
            __ceil__() -> int
            __floor__() -> int
            __trunc__() -> int
            GetDay() -> float or int
            SetDay(day)
            TransformToYear() -> Year
            TransformToMonth() -> Month
            TransformToHour() -> Hour
            TransformToMinute() -> Minute
            TransformToSecond() -> Second
            AddTime(other) -> Day
            SubTime(other) -> Day
            MulTime(other) -> Day
            ToDate() -> Date

        Properties:
            day
            _num (protected)
            _ratio (private)

    Hour(TimeUnit)

        Methods:
            __init__(hour) -> Hour
            __str__() -> str
            __repr__() -> str
            __bool__() -> bool
            __add__(other) -> Hour
            __iadd__(other) -> Hour
            __sub__(other) -> Hour
            __isub__(other) -> Hour
            __mul__(other) -> Hour
            __imul__(other) -> Hour
            __gt__(other) -> bool
            __ge__(other) -> bool
            __lt__(other) -> bool
            __le__(other) -> bool
            __eq__(other) -> bool
            __ne__(other) -> bool
            __call__(num)
            __int__() -> int
            __float__() -> float
            __pos__() -> float or int
            __neg__() -> float or int
            __ceil__() -> int
            __floor__() -> int
            __trunc__() -> int
            GetHour() -> float or int
            SetHour(hour)
            TransformToYear() -> Year
            TransformToMonth() -> Month
            TransformToDay() -> Day
            TransformToMinute() -> Minute
            TransformToSecond() -> Second
            AddTime(other) -> Hour
            SubTime(other) -> Hour
            MulTime(other) -> Hour

        Properties:
            hour
            _num (protected)
            _ratio (private)

    Minute(TimeUnit)

        Methods:
            __init__(minute) -> Minute
            __str__() -> str
            __repr__() -> str
            __bool__() -> bool
            __add__(other) -> Minute
            __iadd__(other) -> Minute
            __sub__(other) -> Minute
            __isub__(other) -> Minute
            __mul__(other) -> Minute
            __imul__(other) -> Minute
            __gt__(other) -> bool
            __ge__(other) -> bool
            __lt__(other) -> bool
            __le__(other) -> bool
            __eq__(other) -> bool
            __ne__(other) -> bool
            __call__(num)
            __int__() -> int
            __float__() -> float
            __pos__() -> float or int
            __neg__() -> float or int
            __ceil__() -> int
            __floor__() -> int
            __trunc__() -> int
            GetMinute() -> float or int
            SetMinute(minute)
            TransformToYear() -> Year
            TransformToMonth() -> Month
            TransformToDay() -> Day
            TransformToHour() -> Hour
            TransformToSecond() -> Second
            AddTime(other) -> Minute
            SubTime(other) -> Minute
            MulTime(other) -> Minute

        Properties:
            minute
            _num (protected)
            _ratio (private)

    Second(TimeUnit)

        Methods:
            __init__(second) -> Second
            __str__() -> str
            __repr__() -> str
            __bool__() -> bool
            __add__(other) -> Second
            __iadd__(other) -> Second
            __sub__(other) -> Second
            __isub__(other) -> Second
            __mul__(other) -> Second
            __imul__(other) -> Second
            __gt__(other) -> bool
            __ge__(other) -> bool
            __lt__(other) -> bool
            __le__(other) -> bool
            __eq__(other) -> bool
            __ne__(other) -> bool
            __call__(num)
            __int__() -> int
            __float__() -> float
            __pos__() -> float or int
            __neg__() -> float or int
            __ceil__() -> int
            __floor__() -> int
            __trunc__() -> int
            GetSecond() -> float or int
            SetSecond(second)
            TransformToYear() -> Year
            TransformToMonth() -> Month
            TransformToDay() -> Day
            TransformToHour() -> Hour
            TransformToMinute() -> Minute
            AddTime(other) -> Second
            SubTime(other) -> Second
            MulTime(other) -> Second

        Properties:
            second
            _num (protected)
            _ratio (private)

    TimeStamp

        Methods:
            __init__(time_stamp_float_number) -> TimeStamp
            __str__() -> str
            __repr__() -> str
            __add__(other) -> TimeStamp
            __sub__(other) -> TimeStamp
            __mul__(other) -> TimeStamp
            __truediv__(other) -> TimeStamp
            __floordiv__(other) -> TimeStamp
            __mod__(other) -> TimeStamp
            __pow__(other) -> TimeStamp
            __lshift__(other) -> TimeStamp
            __rshift__(other) -> TimeStamp
            __iadd__(other) -> TimeStamp
            __isub__(other) -> TimeStamp
            __imul__(other) -> TimeStamp
            __itruediv__(other) -> TimeStamp
            __ifloordiv__(other) -> TimeStamp
            __imod__(other) -> TimeStamp
            __ipow__(other) -> TimeStamp
            __ilshift__(other) -> TimeStamp
            __irshift__(other) -> TimeStamp
            __divmod__(other) -> TimeStamp
            __lt__(other) -> bool
            __le__(other) -> bool
            __gt__(other) -> bool
            __ge__(other) -> bool
            __eq__(other) -> bool
            __ne__(other) -> bool
            __abs__() -> int
            __int__() -> int
            __float__() -> float
            __round__(digit=None) -> int
            __trunc__() -> int
            __floor__() -> int
            __ceil__() -> int
            __pos__() -> TimeStamp
            __neg__() -> TimeStamp
            GetTimeStamp() -> float
            SetTimeStamp(time_stamp_float_number)
            Add(other) -> TimeStamp
            Subtract(other) -> TimeStamp
            Multiply(other) -> TimeStamp
            ToDateTime() -> DateTime
            Clone() -> TimeStamp
            Now() -> TimeStamp
            ToStructTime() -> time.struct_time
            ToDate() -> Date

        Properties:
            time_stamp
            _time_stamp (protected)

    Date
    
        Methods:
            __init__(year, month, day) -> Date
            __add__(other) -> Date
            __iadd__(other) -> Date
            __str__() -> str
            __repr__() -> str
            __int__() -> int
            __float__() -> float
            __lt__(other) -> bool
            __le__(other) -> bool
            __gt__(other) -> bool
            __le__(other) -> bool
            __eq__(other) -> bool
            __ne__(other) -> bool
            GetYear() -> int
            GetMonth() -> int
            GetDay() -> int
            GetWeekDay() -> int (range[0, 6])
            GetYearDay() -> int (range[1, 366])
            SetYear(year)
            SetMonth(month)
            SetDay(day)
            IsLeapYear() -> bool
            ToTimeStamp() -> TimeStamp
            Clone() -> Date
            Now() -> Date
            ToDay() -> Day
            Add(other) -> Date
            GetNextMonthDate() -> Date
            GetNextYearDate() -> Date
            GetNextDayDate() -> Date
            GetPreviousMonthDate() -> Date
            GetPreviousDayDate() -> Date
            GetPreviousYearDate() -> Date
        
        Properties:
            year
            month
            day
            _day (protected)
            _month (protected)
            _year (protected)
            max_day
            max_month
            min_day
            min_month
        
    Calendar

        Methods:
            __init__(first_weekday=0, is_leap_year=False) -> Calendar
            __str__() -> str
            __repr__() -> str
            GetFirstWeekday() -> int (range[0, 6], Monday Is 0)
            GetIsLeapYear() -> bool
            SetFirstWeekDay(first_weekday)
            SetIsLeapYear(is_leap_year)
            GetWeekdayByYearDay(year_day=0) -> int (range[0, 6], Monday Is 0)
            GetWeekdayByMonthAndDay(month=1, day=1) -> int (range[0, 6], Monday Is 0)
            GetCalendarThisYear() -> Calendar
            GetCalendarByYear(year) -> Calendar

        Properties:
            first_weekday
            is_leap_year
            _first_weekday
            _is_leap_year
            max_first_weekday
            min_first_weekday

    Error(Exception)
    
        Methods:
            __init__(reason="") -> Error
            __str__() -> str
            __repr__() -> str
            GetReason() -> str

        Properties:
            reason
            __reason (private)

    UnknownError(Error)
    DateTimeError(Error)
    TimeTableError(Error)
    TimerError(Error)
    StartTimerError(TimerError)
    StopTimerError(TimerError)
    GetTimeError(TimerError)
    TimeUnitError(Error)
    ParseError(Error)
    TransformError(Error)
    TimeStampError(Error)
    FormatError(Error)
    DateError(Error)
    CalendarError(Error)
"""

# import
try:
    import pickle as _pickle
    import math as _math
    import time as _time
    import random as _random
    import calendar as _calendar
    import sys as _sys
except ImportError:
    raise AssertionError('Failed to import module.')

# public variables
datetime_transform_unit_year = 0
datetime_transform_unit_month = 1
datetime_transform_unit_day = 2
datetime_transform_unit_hour = 3
datetime_transform_unit_minute = 4
datetime_transform_unit_second = 5
day_of_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
ver = '1.3.0'
version = ver
major_version = '1'
minor_version = '3'
release_number = '0'
build_type = 'release'


# functions


def Compile(x, y):

    """
    Compile(x, y) -> bool
    If Return 1: x > y
    If Return 0: x == y
    If Return -1: x < y
    parameter x: An Object -> object
    parameter y: An Object -> object
    """
    
    if x > y:
        return 1
    elif x == y:
        return 0
    elif x < y:
        return -1


def FormatTimeNow(format_str='%Y-%m-%d %H:%M:%S'):

    """
    FormatTimeNow(format_str='%Y-%m-%d %H:%M:%S') -> str
    Get The Time Now
    parameter format_str: Reference time Module -> str
    """

    if not type(format_str) == str:
        raise GetTimeError('Unexpected Argument: format_str')

    time1 = _time.strftime(format_str, _time.localtime())
    return time1


def FormatTimeTuple(p_tuple=None):

    """
    FormatTimeTuple(p_tuple=None) -> str
    Convert A Time Tuple To String, e.g. 'Sat Jun 06 16:26:11 1998'
    parameter p_tuple: A Time Tuple (Can Be time.localtime(seconds=None)) -> tuple
    """

    ret = _time.asctime(p_tuple)
    return ret


def FormatTimeStamp(time_stamp=None):

    """
    FormatTimeStamp(time_stamp=None) -> str
    Convert A TimeStamp Object To String, e.g. 'Sat Jun 06 16:26:11 1998'
    parameter time_stamp: A TimeStamp Object -> TimeStamp
    """

    if type(time_stamp) != TimeStamp or time_stamp is not None:
        raise FormatError('Unexpected Argument: time_stamp.')
    if type(time_stamp) == TimeStamp:
        sec = float(time_stamp.GetTimeStamp())
        ret = _time.ctime(sec)
        return ret
    elif time_stamp is None:
        sec = None
        ret = _time.ctime(sec)
        return ret


def FormatDateTime(DateTime=None):

    """
    FormatDateTime(DateTime=None) -> str
    Convert A DateTime Object To String, e.g. 'Sat Jun 06 16:26:11 1998'
    parameter DateTime: A DateTime Object -> DateTime
    """

    time_stamp = None
    if DateTime is not None:
        if type(DateTime) != DateTime:
            raise FormatError('Unexpected Argument: DateTime.')
        else:
            time_stamp = DateTime.ToTimeStamp()
    if type(time_stamp) == TimeStamp:
        sec = float(time_stamp.GetTimeStamp())
        ret = _time.ctime(sec)
        return ret
    elif time_stamp is None:
        sec = None
        ret = _time.ctime(sec)
        return ret


def ParseInt(timeunitobj):

    """
    ParseInt(timeunitobj) -> int
    Transform The TimeUnit Object To Int
    parameter timeunitobj: A TimeUnit Object -> TimeUnit
    """

    if not isinstance(timeunitobj, TimeUnit):
        raise ParseError('parameter timeunitobj is not a current type.')

    return int(timeunitobj._num)


def ParseFloat(timeunitobj):

    """
    ParseFloat(timeunitobj) -> float
    Transform The TimeUnit Object To Float
    parameter timeunitobj: A TimeUnit Object -> TimeUnit
    """

    if not isinstance(timeunitobj, TimeUnit):
        raise ParseError('parameter timeunitobj is not a current type.')

    return float(timeunitobj._num)


def ParseList(DateTimeobj):

    """
    ParseList(DateTimeobj) -> list
    Transform The DateTime Object To List
    parameter DateTimeobj: A DateTime Object -> DateTime
    """

    if not isinstance(DateTimeobj, DateTime):
        raise ParseError('parameter DateTimeobj is not a current type.')

    return DateTimeobj._list


def ParseDict(timetableobj):

    """
    ParseDict(timetableobj) -> dict
    Transform The TimeTable Object To Dict
    parameter timetableobj: A TimeTable Object -> TimeTable
    """

    if not isinstance(timetableobj, TimeTable):
        raise ParseError('parameter timetableobj is not a current type.')

    return timetableobj._dict


def GetTimeNow():

    """
    GetTimeNow() -> str
    Get The Time String Now
    """

    return _time.asctime()


def GetCalendarThisYear():

    """
    GetCalendarThisYear() -> Calendar
    Get Calendar This Year
    """

    return Calendar.GetCalendarThisYear()


def GetCalendarByYear(year):

    """
    GetCalendarByYear(year) -> Calendar
    Get A Calendar By Year
    parameter year: A Year -> int
    """

    return Calendar.GetCalendarByYear(year)


def GetStructTimeNow():

    """
    GetStructTimeNow() -> time.struct_time
    Get The time.struct_time Object Now
    """

    return _time.localtime()


def GetDateTimeNow():

    """
    GetDateTimeNow() -> DateTime
    Get DateTime Now
    """

    return DateTime.Now()


def GetDateNow():

    """
    GetDateNow() -> Date
    Get Date Now
    """

    return Date.Now()


def GetYearNow():

    """
    GetYearNow() -> Year
    Get Year Now
    """

    return Year(DateTime.Now()[0])


def GetMonthNow():

    """
    GetMonthNow() -> Month
    Get Month Now
    """

    return Month(DateTime.Now()[1])


def GetDayNow():

    """
    GetDayNow() -> Day
    Get Day Now
    """

    return Day(DateTime.Now()[2])


def GetHourNow():

    """
    GetHourNow() -> Hour
    Get Hour Now
    """

    return Hour(DateTime.Now()[3])


def GetMinuteNow():

    """
    GetMinuteNow() -> Minute
    Get Minute Now
    """

    return Minute(DateTime.Now()[4])


def GetSecondNow():

    """
    GetSecondNow() -> Second
    Get Second Now
    """

    return Second(DateTime.Now()[5])


def GetTimeStampNow():

    """
    GetTimeStampNow() -> TimeStamp
    Get TimeStamp Now
    """

    return TimeStamp.Now()


def GetDatesIterator(year, month):

    """
    GetDatesIterator(year=None, month=None) -> generator
    parameter year: The Year -> int
    parameter month: The Month -> int (range[1, 12])
    """

    if not (type(year) == int or type(month) == int):
        raise TransformError

    if not 1 <= month <= 12:
        raise TransformError

    iterator = _calendar.Calendar().itermonthdays4(year, month)
    return iterator


def IsLeapYearNow():

    """
    IsLeapYearNow() -> bool
    Acquire Whether This Year Is A Leap Year
    """

    this = DateTime.Now()
    year = this.GetYear()
    return (year % 4 == 0) and (year % 100 != 0)


def RandomDateTime():

    """
    RandomDateTime() -> DateTime
    Generate A Random DateTime From DateTime(0, 0, 0, 0, 0, 0, 0, 0, 0) To DateTime.Now()
    """

    auto = DateTime.Now()
    year = _random.randint(0, auto.GetYear())
    month = _random.randint(0, auto.GetMonth())
    day = _random.randint(0, auto.GetDay())
    hour = _random.randint(0, auto.GetHour())
    minute = _random.randint(0, auto.GetMinute())
    second = _random.randint(0, auto.GetSecond())
    zs = _random.randint(0, auto.GetZeroPointOneSecond())
    zzs = _random.randint(0, auto.GetZeroPointZeroOneSecond())
    zzzs = _random.randint(0, auto.GetZeroPointZeroZeroOneSecond())
    datetime = DateTime(year, month, day, hour, minute, second, zs, zzs, zzzs)
    return datetime


def RandomYear():

    """
    RandomYear() -> Year
    Generate A Random Year From 1970 To Now
    """

    n = DateTime.Now()
    yn = n.GetYear()
    year_num = _random.randint(1970, yn)
    return Year(year_num)


def RandomMonth():

    """
    RandomMonth() -> Month
    Generate A Random Month From 1 To 12
    """

    month_num = _random.randint(1, 12)
    return Month(month_num)


def RandomDay():

    """
    RandomDay() -> Day
    Generate A Random Day From 1 To 30
    """

    d = _random.randint(1, 30)
    return Day(d)


def RandomHour():

    """
    RandomHour() -> Hour
    Generate A Random Hour From 0 To 23
    """

    h = _random.randint(0, 23)
    return Hour(h)


def RandomMinute():

    """
    RandomMinute() -> Minute
    Generate A Random Minute From 0 To 59
    """

    m = _random.randint(0, 59)
    return Minute(m)


def RandomSecond():

    """
    RandomSecond() -> Second
    Generate A Random Second From 0 To 59
    """

    s = _random.randint(0, 59)
    return Second(s)


def OutputCalendarThisYear():

    """
    OutputCalendarThisYear() -> str
    Output The Calendar This Year
    """

    _calendar.main(_sys.argv)


def DaysBeforeYear(year: int):

    """
    DaysBeforeYear(year) -> Day
    Calculate The Days From 1 To The Year
    parameter year: The Year -> int
    """

    y = year - 1
    days = y * 365 + y // 4 - y // 100 + y // 400
    return Day(days)


def DaysInMonth(year, month):

    """
    DayInMonth(year, month) -> Day
    Calculate The Days Of Month
    parameter year: The Year -> int
    parameter month: The Month (range[1, 12]) -> int
    """

    if not (type(year) == int and type(month) == int):
        raise TransformError('Unexpected Argument.')

    if not 1 <= month <= 12:
        raise TransformError('Argument month Should Be 1-12.')

    if month == 2 and Date(year, 1, 1).IsLeapYear():
        return 29
    days = day_of_month[month - 1]
    return Day(days)


def DaysBeforeMonth(year, month):

    """
    DaysBeforeMonth(year, month) -> Day
    Calculate The Days From 1 To month
    parameter year: The Year -> int
    parameter month: The Month (range[1, 12]) -> int
    """

    if not type(year) == int and type(month) == int:
        raise TransformError('Unexpected Argument.')

    if not 1 <= month <= 12:
        raise TransformError('Argument month Should Be 1-12.')

    day = 0
    _day = 0
    dl = []
    if Date(year, 1, 1).IsLeapYear():
        day += 1
    for i in range(12):
        dl.append(_day)
        _day += day_of_month[i]
    day += dl[month - 1]
    return Day(day)


# classes
class DateTime:

    """
    It's a list of time.

    Methods:
        __init__(year=0,
                 month=0,
                 day=0,
                 hour=0,
                 minute=0,
                 second=0,
                 zero_point_one_second=0,
                 zero_point_zero_one_second=0,
                 zero_point_zero_zero_one_second=0) -> DateTime
        __add__(other) -> DateTime
        __iadd__(other) -> DateTime
        __len__() -> int
        __lt__(other) -> bool
        __ne__(other) -> bool
        __ge__(other) -> bool
        __gt__(other) -> bool
        __le__(other) -> bool
        __eq__(other) -> bool
        __iter__() -> list_iterator
        __next__() -> object
        __contains__(item) -> bool
        __getitem__(item) -> int
        __str__() -> str
        __repr__() -> str
        __bool__() -> True
        __format__(format_spec) -> str
        Clone() -> DateTime
        Now() -> DateTime
        SetYear(year)
        SetMonth(month)
        SetDay(day)
        SetHour(hour)
        SetMinute(minute)
        SetSecond(second)
        SetZeroPointOneSecond(zero_point_one_second)
        SetZeroPointZeroOneSecond(zero_point_zero_one_second)
        SetZeroPointZeroZeroOneSecond(zero_point_zero_zero_one_second)
        GetYear() -> int
        GetMonth() -> int
        GetDay() -> int
        GetHour() -> int
        GetMinute() -> int
        GetSecond() -> int
        GetZeroPointOneSecond() -> int
        GetZeroPointZeroOneSecond() -> int
        GetZeroPointZeroZeroOneSecond() -> int
        Transform(unit) -> float
        Difference() -> DateTime
        Format(format_spec) -> str
        GetWeekDay() -> int (range[1, 7], Monday is 0)
        ToTimeStamp() -> TimeStamp
        Add(other) -> DateTime
        IsLeapYear() -> bool
        GetList() -> list
        GetYearDay() -> int (range[1, 366])

    Properties:
        time_list
        year
        month
        day
        hour
        minute
        second
        zero_point_one_second
        zero_point_zero_one_second
        zero_point_zero_zero_one_second
        _list (protected)
        __len (private)
    """

    def __init__(self,
                 year=1970,
                 month=1,
                 day=1,
                 hour=8,
                 minute=0,
                 second=0,
                 zero_point_one_second=0,
                 zero_point_zero_one_second=0,
                 zero_point_zero_zero_one_second=0):

        # no doc

        try:
            int(year)
            int(month)
            int(day)
            int(hour)
            int(minute)
            int(second)
            int(zero_point_one_second)
            int(zero_point_zero_one_second)
            int(zero_point_zero_zero_one_second)
        except ValueError:
            raise DateTimeError

        if (
                year < 1970
                or month > 12
                or month < 1
                or day > 31
                or day < 1
                or hour >= 24
                or hour < 0
                or minute >= 60
                or minute < 0
                or second >= 60
                or second < 0
                or zero_point_one_second > 10
                or zero_point_zero_one_second > 10
                or zero_point_zero_zero_one_second > 10
                or zero_point_one_second < 0
                or zero_point_zero_one_second < 0
                or zero_point_zero_zero_one_second < 0
        ):
            raise DateTimeError("An invalid time.")

        if (
            month == 4
            or month == 6
            or month == 9
            or month == 11
        ) and (
            day >= 30
        ):
            raise DateTimeError("An invalid time.")
        if (
            month == 2
        ) and (
            day > 28
        ):
            if (not year % 4) and (year % 100 != 0):
                pass
            else:
                raise DateTimeError("An invalid time.")

        self._list = [year, month, day, hour, minute, second,
                      zero_point_one_second, zero_point_zero_one_second, zero_point_zero_zero_one_second]
        self.__len = 0

    def __add__(self, other):

        """
        __add__(other) -> DateTime
        DateTime Add DateTime
        """

        try:
            time1 = []
            for i in range(9):
                t = self._list[i] + other._list[i]
                time1.append(t)
            if time1[8] >= 10:
                r = time1[8] // 10
                time1[7] += r
                time1[8] %= 10
            if time1[7] >= 10:
                r = time1[7] // 10
                time1[6] += r
                time1[7] %= 10
            if time1[6] >= 10:
                r = time1[6] // 10
                time1[5] += r
                time1[6] %= 10
            if time1[5] >= 60:
                r = time1[5] // 60
                time1[4] += r
                time1[5] %= 60
            if time1[4] >= 60:
                r = time1[4] // 60
                time1[3] += r
                time1[4] %= 60
            if time1[3] >= 24:
                r = time1[3] // 24
                time1[2] += r
                time1[3] %= 24
            if time1[2] >= 30:
                r = time1[2] // 30
                time1[1] += r
                time1[2] %= 30
            if time1[1] >= 12:
                r = time1[1] // 12
                time1[0] += r
                time1[1] %= 12
            return time1
        except (AttributeError, IndexError):
            raise UnknownError

    def __iadd__(self, other):

        """
        __iadd__(other) -> DateTime
        DateTime Add DateTime
        """

        try:
            time1 = []
            for i in range(9):
                t = self._list[i] + other._list[i]
                time1.append(t)
            if time1[8] >= 10:
                r = time1[8] // 10
                time1[7] += r
                time1[8] %= 10
            if time1[7] >= 10:
                r = time1[7] // 10
                time1[6] += r
                time1[7] %= 10
            if time1[6] >= 10:
                r = time1[6] // 10
                time1[5] += r
                time1[6] %= 10
            if time1[5] >= 60:
                r = time1[5] // 60
                time1[4] += r
                time1[5] %= 60
            if time1[4] >= 60:
                r = time1[4] // 60
                time1[3] += r
                time1[4] %= 60
            if time1[3] >= 24:
                r = time1[3] // 24
                time1[2] += r
                time1[3] %= 24
            if time1[2] >= 30:
                r = time1[2] // 30
                time1[1] += r
                time1[2] %= 30
            if time1[1] >= 12:
                r = time1[1] // 12
                time1[0] += r
                time1[1] %= 12
            return time1
        except (AttributeError, IndexError):
            raise UnknownError

    def __len__(self):

        """
        __len__() -> int
        Get The Length Of List
        """

        return len(self._list)

    def __lt__(self, other):

        """
        __lt__(other) -> bool
        Get self < value
        parameter other: A DateTime Object -> DateTime
        """

        if not type(other) == DateTime:
            raise DateTimeError("The other's type should be DateTime.")
        for i in range(len(self._list)):
            if self._list[i] > other._list[i]:
                return False
            elif self._list[i] < other._list[i]:
                return True
            else:
                continue
        else:
            return False

    def __ne__(self, other):

        """
        __ne__(other) -> bool
        Get self != value
        parameter other: A DateTime Object -> DateTime
        """

        if not self.__eq__(other):
            return True
        else:
            return False

    def __ge__(self, other):

        """
        __ge__(other) -> bool
        Get self >= value
        parameter other: A DateTime Object -> DateTime
        """

        if self.__gt__(other):
            return True

        else:
            if self.__eq__(other):
                return True

            else:
                return False

    def __gt__(self, other):

        """
        __gt__(other) -> bool
        Get self > value
        parameter other: A DateTime Object -> DateTime
        """

        if self.__lt__(other) or self.__eq__(other):
            return False

        else:
            return True

    def __le__(self, other):

        """
        __le__(other) -> bool
        Get self <= value
        parameter other: A DateTime Object -> DateTime
        """

        if self.__lt__(other):
            return True

        else:
            if self.__eq__(other):
                return True
            else:
                return False

    def __eq__(self, other):

        """
        __eq__(other) -> bool
        Get self == value
        parameter other: A DateTime Object -> DateTime
        """

        if not type(other) == DateTime:
            raise DateTimeError("The other's type should be DateTime.")
        if (self._list[0] == other._list[0] and
            self._list[1] == other._list[1] and
            self._list[2] == other._list[2] and
            self._list[3] == other._list[3] and
            self._list[4] == other._list[4] and
            self._list[5] == other._list[5] and
            self._list[6] == other._list[6] and
            self._list[7] == other._list[7] and
            self._list[8] == other._list[8]):
            return True
        else:
            return False

    def __iter__(self):

        """
        __iter__() -> list_iterator
        Get The Iterator
        """

        return iter(self._list)

    def __next__(self):

        """
        __next__() -> object
        Start The Iteration (for x in instance -> DateTime)
        """

        if self.__len > 8:
            self.__len = 0
            raise StopIteration
        else:
            self.__len += 1
            return self._list[self.__len - 1]

    def __contains__(self, item):

        """
        __contains__(item) -> bool
        Get Whether The List Have The Element
        parameter item: The Element Of The List
        """

        return item in self._list

    def __getitem__(self, item):

        """
        __getitem__(item) -> int
        Get The Item Of The DateTime
        """

        return self._list[item]

    def __str__(self):

        """
        __str__() -> str
        Print The List
        """

        return str(self._list)

    def __repr__(self):

        """
        __repr__() -> str
        Print The List
        """

        return str(self._list)

    def __bool__(self):

        """
        __bool__() -> True
        Returns True
        """

        return True

    def __format__(self, format_spec):

        """
        __format__(format_spec) -> str
        You Can Use format() built-in Function To Format It

        Example:
            import timetoolkit
            time = timetoolkit.DateTime(2019, 6, 16, 7, 7, 11, 2, 3, 6)
            print(time.__format__('YYYY-M-DD h:mm:ss.0.1s0.01s0.001s'))
            '2019-6-16 7:33:59.538'
            print(time.__format__('YY-MM-DD hh:mm:ss.0.1s0.01s0.001s'))
            '19-06-16 07:33:59.538'

        parameter format_spec: The Formats String, It Is A String Object
                               It Can Includes 15 Characters -> str

        ========= ===============================================================
        Character Meaning
        --------- ---------------------------------------------------------------
        'YYYY'    The Year Format String
        'YY'      The Year Format String (Show The First Two Digits)
        'MM'      The Month Format String
        'M'       The Month Format String (No zero-padding strings are required)
        'DD'      The Day Format String
        'D'       The Day Format String (No zero-padding strings are required)
        'hh'      The Hour Format String
        'h'       The Hour Format String (No zero-padding strings are required)
        'mm'      The Minute Format String
        'm'       The Minute Format String (No zero-padding strings are required)
        'ss'      The Second Format String
        's'       The Second Format String (No zero-padding strings are required)
        '0.1s'    The 0.1 Second Format String
        '0.01s'   The 0.1 Second Format String
        '0.001s'  The 0.1 Second Format String
        ========= ===============================================================
        """

        if not type(format_spec) == str:
            raise DateTimeError

        format_spec = format_spec.replace('YYYY', str(self._list[0]))
        format_spec = format_spec.replace('YY', str(self._list[0])[:2] if len(str(self._list[0])) >= 2
                                                                       else '0' + str(self._list[0])[0])
        format_spec = format_spec.replace('MM', str(self._list[1]) if len(str(self._list[1])) > 1
                                                                   else '0' + str(self._list[1]))
        format_spec = format_spec.replace('M', str(self._list[1]))
        format_spec = format_spec.replace('DD', str(self._list[2]) if len(str(self._list[2])) > 1
                                                                   else '0' + str(self._list[2]))
        format_spec = format_spec.replace('DD', str(self._list[2]))
        format_spec = format_spec.replace('hh', str(self._list[3]) if len(str(self._list[3])) > 1
                                                                   else '0' + str(self._list[3]))
        format_spec = format_spec.replace('h', str(self._list[3]))
        format_spec = format_spec.replace('mm', str(self._list[4]) if len(str(self._list[4])) > 1
                                                                   else '0' + str(self._list[4]))
        format_spec = format_spec.replace('m', str(self._list[4]))
        format_spec = format_spec.replace('ss', str(self._list[5]) if len(str(self._list[5])) > 1
                                                                   else '0' + str(self._list[5]))
        format_spec = format_spec.replace('s', str(self._list[5]))
        format_spec = format_spec.replace('0.1s', str(self._list[6]))
        format_spec = format_spec.replace('0.01s', str(self._list[7]))
        format_spec = format_spec.replace('0.001s', str(self._list[8]))

        return format_spec

    @property
    def time_list(self):

        """
        Get self._list
        """

        return self._list

    @property
    def year(self):

        """
        Get The Year Of The DateTime
        """

        return self._list[0]

    @property
    def month(self):

        """
        Get The Month Of The DateTime
        """

        return self._list[1]

    @property
    def day(self):

        """
        Get The Day Of The DateTime
        """

        return self._list[2]

    @property
    def hour(self):

        """
        Get The Hour Of The DateTime
        """

        return self._list[3]

    @property
    def minute(self):

        """
        Get The Minute Of The DateTime
        """

        return self._list[4]

    @property
    def second(self):

        """
        Get The Second Of The DateTime
        """

        return self._list[5]

    @property
    def zero_point_one_second(self):

        """
        Get The 0.1 Second Of The DateTime
        """

        return self._list[6]

    @property
    def zero_point_zero_one_second(self):

        """
        Get The 0.01 Second Of The DateTime
        """

        return self._list[7]

    @property
    def zero_point_zero_zero_one_second(self):

        """
        Get The 0.001 Second Of The DateTime
        """

        return self._list[8]

    def Clone(self):

        """
        Clone() -> DateTime
        Clone Self.
        """

        return self

    @staticmethod
    def Now():

        """
        Now() -> DateTime
        Auto Generation Of DateTime (The Time Now)
        """

        time1 = list(_time.localtime())[:6]
        _ = str(_time.time())
        i = _.find('.')
        i = _[i + 1:i + 4]

        for index in range(3):
            time1.append(int(i[index]))
        time_list = DateTime(time1[0],
                             time1[1],
                             time1[2],
                             time1[3],
                             time1[4],
                             time1[5],
                             time1[6],
                             time1[7],
                             time1[8])

        return time_list

    def SetYear(self, year):

        """
        SetYear(year)
        Set The Year Of Your DateTime
        parameter year: The Year You Want To Set -> int
        """

        if type(year) != int:
            raise DateTimeError('Unexpected Argument.')
        if not 0 <= year:
            raise DateTimeError('Unexpected Argument.')
        self._list[0] = year

    def SetMonth(self, month):

        """
        SetMonth(month)
        Set The Month Of Your DateTime
        parameter month: The Month You Want To Set -> int
        """

        if type(month) != int:
            raise DateTimeError('Unexpected Argument.')
        if not 0 <= month < Timer.ratio[1]:
            raise DateTimeError('Unexpected Argument.')
        self._list[1] = month

    def SetDay(self, day):

        """
        SetDay(day)
        Set The Day Of Your DateTime
        parameter day: The Day You Want To Set -> int
        """

        if type(day) != int:
            raise DateTimeError('Unexpected Argument.')
        if not 0 <= day < Timer.ratio[2]:
            raise DateTimeError('Unexpected Argument.')
        self._list[2] = day

    def SetHour(self, hour):

        """
        SetHour(hour)
        Set The Hour Of Your DateTime
        parameter hour: The Hour You Want To Set -> int
        """

        if type(hour) != int:
            raise DateTimeError('Unexpected Argument.')
        if not 0 <= hour < Timer.ratio[3]:
            raise DateTimeError('Unexpected Argument.')
        self._list[3] = hour

    def SetMinute(self, minute):

        """
        SetMinute(minute)
        Set The Minute Of Your DateTime
        parameter minute: The Minute You Want To Set -> int
        """

        if type(minute) != int:
            raise DateTimeError('Unexpected Argument.')
        if not 0 <= minute < Timer.ratio[4]:
            raise DateTimeError('Unexpected Argument.')
        self._list[4] = minute

    def SetSecond(self, second):

        """
        SetSecond(second)
        Set The Second Of Your DateTime
        parameter second: The Second You Want To Set -> int
        """

        if type(second) != int:
            raise DateTimeError('Unexpected Argument.')
        if not 0 <= second < Timer.ratio[5]:
            raise DateTimeError('Unexpected Argument.')
        self._list[5] = second

    def SetZeroPointOneSecond(self, zero_point_one_second):

        """
        SetZeroPointOneSecond(zero_point_one_second)
        Set The 0.1 second Of Your DateTime
        parameter zero_point_one_second: The 0.1 Second You Want To Set -> int
        """

        if type(zero_point_one_second) != int:
            raise DateTimeError('Unexpected Argument.')
        if not 0 <= zero_point_one_second < Timer.ratio[6]:
            raise DateTimeError('Unexpected Argument.')
        self._list[6] = zero_point_one_second

    def SetZeroPointZeroOneSecond(self, zero_point_zero_one_second):

        """
        SetZeroPointZeroOneSecond(zero_point_zero_one_second)
        Set The 0.01 Second Of Your DateTime
        parameter zero_point_zero_one_second: The 0.01 You Want To Set -> int
        """

        if type(zero_point_zero_one_second) != int:
            raise DateTimeError('Unexpected Argument.')
        if not 0 <= zero_point_zero_one_second < Timer.ratio[7]:
            raise DateTimeError('Unexpected Argument.')
        self._list[7] = zero_point_zero_one_second

    def SetZeroPointZeroZeroOneSecond(self, zero_point_zero_zero_one_second):

        """
        SetZeroPointZeroZeroOneSecond(zero_point_zero_zero_one_second)
        Set The 0.001 Second Of Your DateTime
        parameter zero_point_zero_zero_one_second: The Day 0.001 Second Want To Set -> int
        """

        if type(zero_point_zero_zero_one_second) != int:
            raise DateTimeError('Unexpected Argument.')
        if not 0 <= zero_point_zero_zero_one_second < Timer.ratio[8]:
            raise DateTimeError('Unexpected Argument.')
        self._list[8] = zero_point_zero_zero_one_second

    def GetYear(self):

        """
        GetYear() -> int
        Get The Year Of The DateTime
        """

        return self._list[0]

    def GetMonth(self):

        """
        GetMonth() -> int
        Get The Month Of The DateTime
        """

        return self._list[1]

    def GetDay(self):

        """
        GetDay() -> int
        Get The Day Of The DateTime
        """

        return self._list[2]

    def GetHour(self):

        """
        GetHour() -> int
        Get The Hour Of The DateTime
        """

        return self._list[3]

    def GetMinute(self):

        """
        GetMinute() -> int
        Get The Minute Of The DateTime
        """

        return self._list[4]

    def GetSecond(self):

        """
        GetSecond() -> int
        Get The Second Of The DateTime
        """

        return self._list[5]

    def GetZeroPointOneSecond(self):

        """
        GetZeroPointOneSecond() -> int
        Get The 0.1 Second Of The DateTime
        """

        return self._list[6]

    def GetZeroPointZeroOneSecond(self):

        """
        GetZeroPointZeroOneSecond() -> int
        Get The 0.01 Second Of The DateTime
        """

        return self._list[7]

    def GetZeroPointZeroZeroOneSecond(self):

        """
        GetZeroPointZeroZeroOneSecond() -> int
        Get The 0.001 Second Of The DateTime
        """

        return self._list[8]

    def Transform(self, unit):

        """
        Transform(unit) -> float
        Transform the DateTime object to the float
        parameter unit: from timetoolkit.datetime_transform_unit_year to timetoolkit.datetime_transform_unit_second, six orders -> int
        """

        if type(unit) != int:
            raise DateTimeError('An Invalid unit.')

        if not -1 < unit < 6:
            raise DateTimeError('An Invalid unit.')

        if unit == 5:
            second = self._list[5]
            second += self._list[4] * 60
            second += self._list[3] * 60 * 60
            second += self._list[2] * 60 * 60 * 24
            second += self._list[1] * 60 * 60 * 24 * 30
            second += self._list[0] * 60 * 60 * 24 * 30 * 12
            return second

        elif unit == 4:
            minute = self._list[4]
            minute += self._list[5] / 60
            minute += self._list[3] * 60
            minute += self._list[2] * 60 * 24
            minute += self._list[1] * 60 * 24 * 30
            minute += self._list[0] * 60 * 24 * 30 * 12
            return minute

        elif unit == 3:
            hour = self._list[3]
            hour += self._list[5] / 60 / 60
            hour += self._list[4] / 60
            hour += self._list[2] * 24
            hour += self._list[1] * 24 * 30
            hour += self._list[0] * 24 * 30 * 12
            return hour

        elif unit == 2:
            day = self._list[2]
            day += self._list[5] / 60 / 60 / 24
            day += self._list[4] / 60 / 24
            day += self._list[3] / 24
            day += self._list[1] * 30
            day += self._list[0] * 30 * 12
            return day

        elif unit == 1:
            month = self._list[1]
            month += self._list[5] / 60 / 60 / 24 / 30
            month += self._list[4] / 60 / 24 / 30
            month += self._list[3] / 24 / 30
            month += self._list[2] / 30
            month += self._list[0] * 12

        elif unit == 0:
            year = self._list[0]
            year += self._list[5] / 60 / 60 / 24 / 30 / 12
            year += self._list[4] / 60 / 24 / 30 / 12
            year += self._list[3] / 24 / 30 / 12
            year += self._list[2] / 30 / 12
            year += self._list[1] / 12
            return year

    def Difference(self):

        """
        Difference() -> list
        The Difference Between List And The Time Now -> list
        """

        _ = str(_time.time())
        i = _.find('.')
        i = _[i + 1:i + 4]
        time2 = _time.localtime()
        time2 = list(time2)[:6]
        for index in range(3):
            time2.append(int(i[index]))
        a = str(self._list)
        a = a.replace('[', '')
        a = a.replace(']', '')
        a = a.replace(',', '')
        a = a.replace(' ', '')
        a = int(a)
        b = str(time2)
        b = b.replace('[', '')
        b = b.replace(']', '')
        b = b.replace(',', '')
        b = b.replace(' ', '')
        b = int(b)
        c = a > b
        time = []
        if c:
            for index in range(9):
                num = self._list[index] - time2[index]
                if True:
                    if num < 0:
                        num = int(self._list[index] + Timer.ratio[index] - time2[index])
                        self._list[index - 1] -= 1
                time.append(num)
        else:
            for index in range(9):
                num = time2[index] - self._list[index]
                if True:
                    if num < 0:
                        num = int(time2[index] + Timer.ratio[index] - self._list[index])
                        time[index - 1] -= 1
                time.append(num)

        return DateTime(
            time[0],
            time[1],
            time[2],
            time[3],
            time[4],
            time[5],
            time[6],
            time[7],
            time[8]
        )

    def Format(self, format_spec):

        """
        Format(format_spec) -> str
        Format The DateTime

        Example:
            import timetoolkit
            time = timetoolkit.DateTime(2019, 6, 16, 7, 7, 11, 2, 3, 6)
            print(time.__format__('YYYY-M-DD h:mm:ss.0.1s0.01s0.001s'))
            '2019-6-16 7:33:59.538'
            print(time.__format__('YY-MM-DD hh:mm:ss.0.1s0.01s0.001s'))
            '19-06-16 07:33:59.538'

        parameter format_spec: The Formats String, It Is A String Object
                               It Can Includes 15 Characters -> str

        ========= ===============================================================
        Character Meaning
        --------- ---------------------------------------------------------------
        'YYYY'    The Year Format String
        'YY'      The Year Format String (Show The First Two Digits)
        'MM'      The Month Format String
        'M'       The Month Format String (No zero-padding strings are required)
        'DD'      The Day Format String
        'D'       The Day Format String (No zero-padding strings are required)
        'hh'      The Hour Format String
        'h'       The Hour Format String (No zero-padding strings are required)
        'mm'      The Minute Format String
        'm'       The Minute Format String (No zero-padding strings are required)
        'ss'      The Second Format String
        's'       The Second Format String (No zero-padding strings are required)
        '0.1s'    The 0.1 Second Format String
        '0.01s'   The 0.1 Second Format String
        '0.001s'  The 0.1 Second Format String
        ========= ===============================================================
        """

        if not type(format_spec) == str:
            raise DateTimeError

        format_spec = format_spec.replace('YYYY', str(self._list[0]))
        format_spec = format_spec.replace('YY', str(self._list[0])[:2] if len(str(self._list[0])) >= 2
                                                                       else '0' + str(self._list[0])[0])
        format_spec = format_spec.replace('MM', str(self._list[1]) if len(str(self._list[1])) > 1
                                                                   else '0' + str(self._list[1]))
        format_spec = format_spec.replace('M', str(self._list[1]))
        format_spec = format_spec.replace('DD', str(self._list[2]) if len(str(self._list[2])) > 1
                                                                   else '0' + str(self._list[2]))
        format_spec = format_spec.replace('DD', str(self._list[2]))
        format_spec = format_spec.replace('hh', str(self._list[3]) if len(str(self._list[3])) > 1
                                                                   else '0' + str(self._list[3]))
        format_spec = format_spec.replace('h', str(self._list[3]))
        format_spec = format_spec.replace('mm', str(self._list[4]) if len(str(self._list[4])) > 1
                                                                   else '0' + str(self._list[4]))
        format_spec = format_spec.replace('m', str(self._list[4]))
        format_spec = format_spec.replace('ss', str(self._list[5]) if len(str(self._list[5])) > 1
                                                                   else '0' + str(self._list[5]))
        format_spec = format_spec.replace('s', str(self._list[5]))
        format_spec = format_spec.replace('0.1s', str(self._list[6]))
        format_spec = format_spec.replace('0.01s', str(self._list[7]))
        format_spec = format_spec.replace('0.001s', str(self._list[8]))

        return format_spec

    def GetWeekDay(self):

        """
        GetWeekDay() -> int (range[1, 7], Monday is 0)
        Get The WeekDay Number Of The DateTime Object
        """

        ts_float = self.ToTimeStamp().GetTimeStamp()
        st = _time.localtime(ts_float)
        return st.tm_wday + 1

    def ToTimeStamp(self):

        """
        ToTimeStamp() -> TimeStamp
        Transform The DateTime Object To Time Stamp
        """

        if (self._list[0] < 1970 or
           (self._list[0] == 1970 and self._list[3] < 8)):
            raise DateTimeError
        year = self._list[0]
        month = self._list[1]
        day = self._list[2]
        hour = self._list[3]
        minute = self._list[4]
        second = self._list[5]
        zs = self._list[6]
        zzs = self._list[7]
        zzzs = self._list[8]
        is_ly = Date(year, 1, 1).IsLeapYear()
        year -= 1970
        month -= 1
        day -= 1
        hour -= 8
        ts = 0

        if is_ly:
            ts += year * 60 * 60 * 24 * 366
            ts += DaysBeforeMonth(year, month).GetDay() * 60 * 60 * 24
        else:
            ts += year * 60 * 60 * 24 * 365
            ts += DaysBeforeMonth(year, month).GetDay() * 60 * 60 * 24
        ts += day * 60 * 60 * 24
        ts += hour * 60 * 60
        ts += minute * 60
        ts += second
        tist = TimeStamp(ts)

        return tist

    def Add(self, other):

        """
        Add(other) -> DateTime
        DateTime Add DateTime
        """

        try:
            time1 = []
            for i in range(9):
                t = self._list[i] + other._list[i]
                time1.append(t)
            if time1[8] >= 10:
                r = time1[8] // 10
                time1[7] += r
                time1[8] %= 10
            if time1[7] >= 10:
                r = time1[7] // 10
                time1[6] += r
                time1[7] %= 10
            if time1[6] >= 10:
                r = time1[6] // 10
                time1[5] += r
                time1[6] %= 10
            if time1[5] >= 60:
                r = time1[5] // 60
                time1[4] += r
                time1[5] %= 60
            if time1[4] >= 60:
                r = time1[4] // 60
                time1[3] += r
                time1[4] %= 60
            if time1[3] >= 24:
                r = time1[3] // 24
                time1[2] += r
                time1[3] %= 24
            if time1[2] >= 30:
                r = time1[2] // 30
                time1[1] += r
                time1[2] %= 30
            if time1[1] >= 12:
                r = time1[1] // 12
                time1[0] += r
                time1[1] %= 12
            return time1
        except (AttributeError, IndexError):
            raise UnknownError

    def IsLeapYear(self):

        """
        IsLeapYear() -> bool
        Get Whether The DateTime Is Leap Year
        """

        year = self.GetYear()
        b = year % 4 == 0
        b2 = year % 100 != 0
        b = b and b2
        return b

    def GetList(self):

        """
        GetList() -> list
        Get self._list
        """

        return self._list

    def GetYearDay(self):

        """
        GetYearDay() -> int (range[1, 366])
        Get The DateTime's Day Number Of The DateTime's Year
        """

        tsobj = self.ToTimeStamp()
        tsfloat = tsobj.GetTimeStamp()
        st = _time.localtime(tsfloat)
        ret = st.tm_mday
        return ret


class TimeTable:

    """
    Define The TimeTable Class.

    Methods:
        __init__(time_table_dict) -> TimeTable
        __str__() -> str
        __repr__() -> str
        __bool__() -> bool
        __contains__(item) -> bool
        __len__() -> int
        __reversed__() -> TimeTable
        Add(time, action)
        AddMany(time_table_dict)
        Clone() -> TimeTable
        Remove(time)
        RemoveMany(*times)
        Get(time, default='') -> str
        GetMany(*times, default="") -> str
        GetTimes() -> list
        GetActions() -> list
        Clear()
        Set(time, action, default_action='')
        IsEmpty() -> bool
        CreateFile(table_name, location)
        OpenFile(file) -> TimeTable
        CheckExpire(time) -> bool
        Items() -> list
        Reverse() -> TimeTable

    Properties:
        dict
        _dict (provided)
    """

    def __init__(self, time_table_dict):

        """
        __init__(time_table_dict) -> TimeTable
        Define Your Time Table
        parameter time_table_dict: A Dictionary Like That: {DateTime(x, y, z): 'Action', DateTime(a, b, c): 'Action'} -> dict
        """

        if not type(time_table_dict) == dict:
            raise TimeTableError('Unexpected Time Table.')

        for k in time_table_dict.keys():
            if not type(k) == DateTime:
                raise TimeTableError('Unexpected Time Table.')

        for v in time_table_dict.values():
            if type(v) != str:
                raise TimeTableError('Unexpected Time Table.')

        self._dict = time_table_dict

    def __str__(self):

        """
        __str__() -> dict
        A Dictionary Of Your Time Table
        """

        return self._dict

    def __repr__(self):

        """
        __repr__() -> dict
        A Dictionary Of Your Time Table
        """

        return self._dict

    def __bool__(self):

        """
        __bool__() -> bool
        Get Whether The TimeTable Have Any Items
        """

        if self._dict:
            return True
        else:
            return False

    def __contains__(self, item):

        """
        __contains__(item) -> bool
        Get Whether The TimeTable Have The Element
        parameter item: The Element Of The List
        """

        return item in list(self._dict.keys()) or item in list(self._dict.values())

    def __len__(self):

        """
        __len__() -> int
        Get The TimeTable's Length
        """

        return len(self._dict)

    def __reversed__(self):

        """
        __reversed__() -> TimeTable
        Reverse Self
        """

        return dict(zip(list(reversed(self._dict.keys())), list(reversed(self._dict.values()))))

    @property
    def dict(self):

        """
        Get The Dictionary Of Your Time Table
        """

        return self._dict

    def Add(self, time, action):

        """
        Add(time, action)
        Add A Record Into Your Time Table
        parameter time: A DateTime Object -> DateTime
        parameter action: Your Action What You Will Do At The Time -> str
        """

        if not isinstance(DateTime, time):
            raise TimeTableError('Unexpected record.')

        if type(action) != str:
            raise TimeTableError('Unexpected record.')

        for k in list(self._dict.keys()):
            if k == time:
                raise TimeTableError('Unexpected record.')

        self._dict[time] = action

    def AddMany(self, time_table_dict):

        """
        AddMany(time_table_dict)
        Add Many Records Into Your Time Table
        parameter time_table_dict: A Dictionary Like That: {DateTime(x, y, z): 'Thing', DateTime(a, b, c): 'Thing'} -> dict
        """

        if not type(time_table_dict) == dict:
            raise TimeTableError('Unexpected time table.')

        for k in time_table_dict.keys():
            if not isinstance(DateTime, k):
                raise TimeTableError('Unexpected time table.')

        for v in time_table_dict.values():
            if type(v) != str:
                raise TimeTableError('Unexpected time Table')

        for k in time_table_dict.keys():
            if self._dict.get(k, None) is not None:
                raise TimeTableError('Unexpected record.')

        for i in range(len(time_table_dict.keys())):
            self._dict[time_table_dict.keys()[i]] = time_table_dict.values()[i]

    def Clone(self):

        """
        Clone() -> TimeTable
        Clone Self.
        """

        return self

    def Remove(self, time):

        """
        Remove(time)
        Remove The Action What You Do At The Time
        parameter time: A DateTime Object -> DateTime
        """

        try:
            del self._dict[time]
        except KeyError:
            raise TimeTableError('Unexpected key.')

    def RemoveMany(self, *times):

        """
        RemoveMany(*times)
        Remove Times
        parameter times: Many DateTime Object What You Want To Delete -> DateTime
        """

        try:
            for each in times:
                del self._dict[each]
        except KeyError:
            raise TimeTableError('Unexpected keys.')

    def Get(self, time, default=''):

        """
        Get(time, default='') -> str
        Get The Action What You Do At The Time
        parameter time: A DateTime Object -> DateTime
        parameter default: Set The Default Value When The TimeTable Don't Have The Current Value -> str
        """

        if type(default) != str:
            raise TimeTableError('Unexpected "default" Argument. Its type should be string.')
        try:
            return self._dict[time]
        except KeyError:
            return default

    def GetMany(self, *times, default=""):

        """
        GetMany(*times, default="") -> str
        Get The Action What You Do At The Time
        parameter times: A DateTime Object -> DateTime
        parameter default: Set The Default Value When The TimeTable Don't Have The Current Value -> str
        """

        if type(default) != str:
            raise TimeTableError('Unexpected "default" Argument. Its type should be string.')
        __ = []
        for each in times:
            __.append(self.Get(each, default))

        return __

    def GetTimes(self):

        """
        GetTimes() -> list
        Get The Time Of The TimeTable
        """

        return list(list(self._dict.keys()))

    def GetActions(self):

        """
        GetActions() -> list
        Get The Actions Of The TimeTable
        """

        return list(list(self._dict.values()))

    def Clear(self):

        """
        Clear()
        Clear The Time Table
        """

        self._dict = {}

    def Set(self, time, action, default_action=''):

        """
        Set(time, action, default_action='')
        Set The Action What You Do At The Time
        parameter time: A DateTime Object -> DateTime
        parameter action: The Action What You Do At The Time -> str
        parameter default_action: Set The Default Action When The TimeTable Don't Have The Key You Want -> str
        """

        if type(default_action) != str:
            raise TimeTableError('Unexpected "default_action" Argument. Its type should be string.')
        try:
            a = self._dict[time]
        except KeyError:
            self._dict[time] = default_action
        else:
            del a
            self._dict[time] = action

    def IsEmpty(self):

        """
        IsEmpty() -> bool
        Get Whether The TimeTable Have Any Items
        """

        if self._dict:
            return True
        else:
            return False

    def CreateFile(self, table_name, location):

        """
        CreateFile(table_name, location)
        Create A Time Table File And Save Your Time Table Into The File
        parameter table_name: The File Name -> str
        parameter location: The Location Of The File -> str
        """

        try:
            file = open(location + '/' + table_name + '.tt', 'wb')
        except ValueError:
            raise TimeTableError('Unexpected Table Name.')
        except (OSError, IOError):
            raise TimeTableError('Unexpected Location.')
        else:
            _pickle.dump(self, file)

    @staticmethod
    def OpenFile(file):

        """
        OpenFile(file) -> TimeTable
        Open A .tc(TimeTable) File And Read It
        parameter file: A TextIOWrapper Object Which's Mode Must Be 'rb' -> _io.TextIOWrapper
        """

        if not file.name.endswith('.tt'):
            raise TimeTableError('This is not a .tt file.')

        obj = _pickle.load(file)
        if not type(obj) == TimeTable:
            raise TimeTableError('This is not a current time table file.')

        return obj

    def CheckExpire(self, time):

        """
        CheckExpire(time) -> bool
        Check Whether The TimeTable's Time Is Expire
        parameter time: The Time What You Want To Check -> DateTime
        """

        if time not in self._dict:
            raise TimeTableError('Unexpected Type Of Argument: time.')
        
        tl1 = DateTime.Now()
        if time > tl1:
            return True
        
        else:
            return False

    def Items(self):

        """
        Items() -> list
        Get The TimeTable's Items
        """

        return list(zip(list(self._dict.keys()), list(self._dict.values())))

    def Reverse(self):

        """
        Reverse() -> TimeTable
        Reverse Self
        """

        return dict(zip(list(reversed(self._dict.keys())), list(reversed(self._dict.values()))))


class Timer:

    """
    Define The Timer Object.
    
    Methods:
        __str__() -> str
        __add__(other) -> list
        __repr__() -> DateTime
        __lt__(other) -> bool
        __ne__(other) -> bool
        __ge__(other) -> bool
        __gt__(other) -> bool
        __le__(other) -> bool
        __eq__(other) -> bool
        Start()
        Stop()
        IsRunning() -> bool
        GetTime() -> DateTime
    
    Properties:
        running
        ___time (private)
        _time_list (provided)
        is_start
        is_stop
        ratio
        time
        timer_start
        timer_stop
    """

    # Define Class Variables
    is_start = False
    is_stop = True
    time = []
    ratio = [0, 12, 30, 24, 60, 60, 10, 10, 10]
    
    # no __init__ Methods
    
    def __str__(self):

        """
        __str__() -> DateTime
        The Time Of Timer
        """

        return str(self.time)

    def __add__(self, other):

        """
        __add__(other) -> list
        Timer Add Timer
        """

        try:
            time1 = []
            for i in range(9):
                t = self.time[i] + other.time[i]
                time1.append(t)
            if time1[8] >= 10:
                r = time1[8] // 10
                time1[7] += r
                time1[8] %= 10
            if time1[7] >= 10:
                r = time1[7] // 10
                time1[6] += r
                time1[7] %= 10
            if time1[6] >= 10:
                r = time1[6] // 10
                time1[5] += r
                time1[6] %= 10
            if time1[5] >= 60:
                r = time1[5] // 60
                time1[4] += r
                time1[5] %= 60
            if time1[4] >= 60:
                r = time1[4] // 60
                time1[3] += r
                time1[4] %= 60
            if time1[3] >= 24:
                r = time1[3] // 24
                time1[2] += r
                time1[3] %= 24
            if time1[2] >= 30:
                r = time1[2] // 30
                time1[1] += r
                time1[2] %= 30
            if time1[1] >= 12:
                r = time1[1] // 12
                time1[0] += r
                time1[1] %= 12
            return time1
        except (AttributeError, IndexError):
            raise UnknownError

    def __repr__(self):

        """
        __repr__() -> DateTime
        Print The Time of Timer
        """

        return str(self.time)

    def __lt__(self, other):

        """
        __lt__(other) -> bool
        Get self < value
        parameter other: A DateTime Object -> DateTime
        """

        if not type(other) == Timer:
            raise TimerError("The other's type should be DateTime.")
        if self._time_list < other._time_list:
            return True
        else:
            return False

    def __ne__(self, other):

        """
        __ne__(other) -> bool
        Get self != value
        parameter other: A DateTime Object -> DateTime
        """

        if not self.__eq__(other):
            return True
        else:
            return False

    def __ge__(self, other):

        """
        __ge__(other) -> bool
        Get self >= value
        parameter other: A DateTime Object -> DateTime
        """

        if self.__gt__(other):
            return True

        else:
            if self.__eq__(other):
                return True

            else:
                return False

    def __gt__(self, other):

        """
        __gt__(other) -> bool
        Get self > value
        parameter other: A DateTime Object -> DateTime
        """

        if self.__lt__(other) or self.__eq__(other):
            return False

        else:
            return True

    def __le__(self, other):

        """
        __le__(other) -> bool
        Get self <= value
        parameter other: A DateTime Object -> DateTime
        """

        if self.__lt__(other):
            return True

        else:
            if self.__eq__(other):
                return True
            else:
                return False

    def __eq__(self, other):

        """
        __eq__(other) -> bool
        Get self == value
        parameter other: A DateTime Object -> DateTime
        """

        if self._time_list == other._time_list:
            return True
        else:
            return False

    @property
    def running(self):

        """
        Get Whether The Timer Is Running
        """

        return self.is_start

    def Start(self):

        """
        Start()
        Start the timer
        """

        if not self.is_stop:
            raise StartTimerError("You've turned on the Timer!")
        self.__time = []
        _ = str(_time.time())
        i = _.find('.')
        i = _[i + 1:i + 4]
        self.timer_start = _time.localtime()
        self.timer_start = list(self.timer_start)[:6]
        for index in range(3):
            self.timer_start.append(int(i[index]))
        self.is_start = True
        self.is_stop = False

    def Stop(self):

        """
        Stop()
        Stop the timer
        """

        if self.is_stop:
            raise StopTimerError("You've stopped the Timer!")
        _ = str(_time.time())
        i = _.find('.')
        i = _[i + 1:i + 4]
        self.timer_stop = _time.localtime()
        self.timer_stop = list(self.timer_stop)[:6]
        for index in range(3):
            self.timer_stop.append(int(i[index]))
        self.is_stop = True
        self.is_start = False
        for index in range(9):
            num = self.timer_stop[index] - self.timer_start[index]
            if True:
                if num < 0:
                    num = int(self.timer_stop[index] + self.ratio[index] - self.timer_start[index])
                    self.__time[index - 1] -= 1
            self.__time.append(num)
        self._time_list = DateTime(self.__time[0],
                                self.__time[1],
                                self.__time[2],
                                self.__time[3],
                                self.__time[4],
                                self.__time[5],
                                self.__time[6],
                                self.__time[7],
                                self.__time[8])

    def IsRunning(self):

        """
        IsRunning() -> bool
        Get Whether The Timer Is Running
        """

        return self.is_start

    def GetTime(self):

        """
        GetTime() -> DateTime
        Get The Time Of Timer
        """

        if not self.is_start:
            raise GetTimeError("You didn't turned on the Timer!")
        return self.time


class TimeUnit:

    """
    The Base Class For Time Units In This Module.

    You Can Also Customize The Unit Of Time, As Long As The Class Must
    Inherit From The TimeUnit Class In The timetoolkit Package, And The
    Class Must Have __init__ Methods, Must Have Only One Parameter,
    Must Define Two Attributes In __init__ Methods, Namely _num And
    _ratio.

    Example:
        import timetoolkit
        class TimeUnit(timetoolkit.TimeUnit):
            def __init__(self, num):
                self._num = num
                self._ratio = 10    # It Shows How Many Seconds Does The Unit Of Time Contain.

    Then The TimeUnit Object Is A Valid Time Unit Object, And It Can
    Also Be Added, Subtracted, Multiplied And Compared With The Six
    Basic Time Units Contained In The Package.
    
    Methods:
        __init__(num=0) -> TimeUnit
        __str__() -> str
        __repr__() -> str
        __bool__() -> bool
        __add__(other) -> TimeUnit
        __iadd__(other) -> TimeUnit
        __sub__(other) -> TimeUnit
        __isub__(other) -> TimeUnit
        __mul__(other) -> TimeUnit
        __imul__(other) -> TimeUnit
        __gt__(other) -> bool
        __ge__(other) -> bool
        __lt__(other) -> bool
        __le__(other) -> bool
        __eq__(other) -> bool
        __ne__(other) -> bool
        __call__(num)
        __int__() -> int
        __float__() -> float
        __pos__() -> float or int
        __neg__() -> float or int
        __ceil__() -> int
        __floor__() -> int
        __trunc__() -> int

    Properties:
        _num
        _ratio
    """

    def __init__(self, num=0):

        # no doc

        self._num = num         # default number
        self._ratio = 10        # default ratio

    def __str__(self):

        """
        __str__() -> str
        Get self._num
        """

        return str(self._num)

    def __repr__(self):

        """
        __repr__() -> str
        Get self._num
        """

        return str(self._num)

    def __bool__(self):

        """
        __bool__() -> bool
        Get Whether self._num Is 0
        """

        return bool(self._num)

    def __add__(self, other):

        """
        __add__(other) -> TimeUnit
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio)

    def __iadd__(self, other):

        """
        __iadd__(other) -> TimeUnit
        Get Self And Other
        parameter other: self + other -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio)

    def __sub__(self, other):

        """
        __sub__(other) -> TimeUnit
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio)

    def __isub__(self, other):

        """
        __isub__(other) -> TimeUnit
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio)

    def __mul__(self, other):

        """
        __mul__(other) -> TimeUnit
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * other)

    def __imul__(self, other):

        """
        __imul__(other) -> TimeUnit
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * other)

    def __gt__(self, other):

        """
        __gt__(other) -> bool
        Get Self > Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio > other._num * other._ratio

    def __ge__(self, other):

        """
        __ge__(other) -> bool
        Get Self >= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio >= other._num * other._ratio

    def __lt__(self, other):

        """
        __lt__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio < other._num * other._ratio

    def __le__(self, other):

        """
        __le__(other) -> bool
        Get Self <= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio <= other._num * other._ratio

    def __eq__(self, other):

        """
        __eq__(other) -> bool
        Get Self == Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio == other._num * other._ratio

    def __ne__(self, other):

        """
        __ne__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio != other._num * other._ratio

    def __call__(self, num):

        """
        __call__(num)
        Set self._num
        param num: The Number You Want To Set
        """

        if type(num) != int:
            raise TimeUnitError('Unexpected Year: {:s}'.format(str(num)))
        self._num = num

    def __int__(self):

        """
        __int__() -> int
        Get int(self._num)
        """

        return int(self._num)

    def __float__(self):

        """
        __float__() -> float
        Get float(self._num)
        """

        return float(self._num)

    def __pos__(self):

        """
        __pos__() -> float or int
        Get + self._num
        """

        return + self._num

    def __neg__(self):

        """
        __neg__() -> float or int
        Get - self._num
        """

        return - self._num

    def __ceil__(self):

        """
        __ceil__() -> int
        Get math.ceil(self._num)
        """

        return _math.ceil(self._num)

    def __floor__(self):

        """
        __floor__() -> int
        Get math.floor(self._num)
        """

        return _math.floor(self._num)

    def __trunc__(self):

        """
        __trunc__() -> int
        Get math.trunc(self._num)
        """
        
        return _math.trunc(self._num)


class Year(TimeUnit):

    """
    Define The 'Year' Object.

    Methods:
        __init__(num=0) -> Year
        __str__() -> str
        __repr__() -> str
        __bool__() -> bool
        __add__(other) -> TimeUnit
        __iadd__(other) -> TimeUnit
        __sub__(other) -> TimeUnit
        __isub__(other) -> TimeUnit
        __mul__(other) -> TimeUnit
        __imul__(other) -> TimeUnit
        __gt__(other) -> bool
        __ge__(other) -> bool
        __lt__(other) -> bool
        __le__(other) -> bool
        __eq__(other) -> bool
        __ne__(other) -> bool
        __call__(num)
        __int__() -> int
        __float__() -> float
        __pos__() -> float or int
        __neg__() -> float or int
        __ceil__() -> int
        __floor__() -> int
        __trunc__() -> int
        SetYear(year)
        GetYear() -> float or int
        TransformToMonth() -> Month
        TransformToDay() -> Day
        TransformToHour() -> Hour
        TransformToMinute() -> Minute
        TransformToSecond() -> Second
        AddTime(other) -> Year
        SubTime(other) -> Year
        MulTime(other) -> Year

    Properties:
        year
        _num (protected)
        _ratio (protected)
    """

    def __init__(self, year):

        """
        __init__(year) -> Year
        Define The 'Year' Object For You
        parameter year: The Year, Includes Century, e.g. 2019 -> float or int
        """

        super().__init__()
        if type(year) != int and type(year) != float:
            raise TimeUnitError('Unexpected Year: {:s}'.format(str(year)))
        self._num = year
        self._ratio = 60 * 60 * 24 * 30 * 12

    def __str__(self):

        """
        __str__() -> str
        Get self._num
        """

        return str(self._num)

    def __repr__(self):

        """
        __repr__() -> str
        Get self._num
        """

        return str(self._num)

    def __bool__(self):

        """
        __bool__() -> bool
        Get Whether self._num Is 0
        """

        return bool(self._num)

    def __add__(self, other):

        """
        __add__(other) -> Year
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToYear()

    def __iadd__(self, other):

        """
        __add__(other) -> Year
        Get Self And Other
        parameter other: self + other -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToYear()

    def __sub__(self, other):

        """
        __sub__(other) -> Year
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToYear()

    def __isub__(self, other):

        """
        __isub__(other) -> Year
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToYear()

    def __mul__(self, other):

        """
        __mul__(other) -> Year
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Year(self._num * other)

    def __imul__(self, other):

        """
        __imul__(other) -> Year
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Year(self._num * other)

    def __gt__(self, other):

        """
        __gt__(other) -> bool
        Get Self > Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio > other._num * other._ratio

    def __ge__(self, other):

        """
        __ge__(other) -> bool
        Get Self >= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio >= other._num * other._ratio

    def __lt__(self, other):

        """
        __lt__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio < other._num * other._ratio

    def __le__(self, other):

        """
        __le__(other) -> bool
        Get Self <= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio <= other._num * other._ratio

    def __eq__(self, other):

        """
        __eq__(other) -> bool
        Get Self == Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio == other._num * other._ratio

    def __ne__(self, other):

        """
        __ne__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio != other._num * other._ratio

    def __call__(self, num):

        """
        __call__(num)
        Set self._num
        param num: The Number You Want To Set
        """

        if type(num) != int:
            raise TimeUnitError('Unexpected Year: {:s}'.format(str(num)))
        self._num = num

    def __int__(self):

        """
        __int__() -> int
        Get int(self._num)
        """

        return int(self._num)

    def __float__(self):

        """
        __float__() -> float
        Get float(self._num)
        """

        return float(self._num)

    def __pos__(self):

        """
        __pos__() -> float or int
        Get +self._num
        """

        return + self._num

    def __neg__(self):

        """
        __neg__() -> float or int
        Get -self._num
        """

        return - self._num

    def __ceil__(self):

        """
        __ceil__() -> int
        Get math.ceil(self._num)
        """

        return _math.ceil(self._num)

    def __floor__(self):

        """
        __floor__() -> int
        Get math.floor(self._num)
        """

        return _math.floor(self._num)

    def __trunc__(self):

        """
        __trunc__() -> int
        Get math.trunc(self._num)
        """

        return _math.trunc(self._num)

    @property
    def year(self):

        """
        Get The Object's Year
        """

        return self._num

    def SetYear(self, year):

        """
        SetYear(year)
        Set The Object's Year
        parameter year: The Year You Want To Set -> float or int
        """

        if type(year) != int:
            raise TimeUnitError('Unexpected Year: {:s}'.format(str(year)))
        self._num = year

    def GetYear(self):

        """
        GetYear() -> float or int
        Get The Object's Year
        """

        return self._num

    def TransformToMonth(self):

        """
        TransformToMonth() -> Month
        Transform The Year To Month
        """

        return Month(self._num * 12)

    def TransformToDay(self):

        """
        TransformToDay() -> Day
        Transform The Year To Day
        """

        return Day(self._num * 12 * 30)

    def TransformToHour(self):

        """
        TransformToHour() -> Hour
        Transform The Year To Hour
        """

        return Hour(self._num * 12 * 30 * 24)

    def TransformToMinute(self):

        """
        TransformToMinute() -> Minute
        Transform The Year To Minute
        """

        return Minute(self._num * 12 * 30 * 24 * 60)

    def TransformToSecond(self):

        """
        TransformToSecond() -> Second
        Transform The Year To Second
        """

        return Second(self._num * 60 * 60 * 24 * 30 * 12)

    def AddTime(self, other):

        """
        AddTime(other) -> Year
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToYear()

    def SubTime(self, other):

        """
        SubTime(other) -> Year
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToYear()

    def MulTime(self, other):

        """
        MulTime(other) -> Year
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Year(self._num * other)


class Month(TimeUnit):

    """
    Define The 'Month' Object.

    Methods:
        __init__(month) -> Month
        __str__() -> str
        __repr__() -> str
        __bool__() -> bool
        __add__(other) -> Month
        __iadd__(other) -> Month
        __sub__(other) -> Month
        __isub__(other) -> Month
        __mul__(other) -> Month
        __imul__(other) -> Month
        __gt__(other) -> bool
        __ge__(other) -> bool
        __lt__(other) -> bool
        __le__(other) -> bool
        __eq__(other) -> bool
        __ne__(other) -> bool
        __call__(num)
        __int__() -> int
        __float__() -> float
        __pos__() -> float or int
        __neg__() -> float or int
        __ceil__() -> int
        __floor__() -> int
        __trunc__() -> int
        GetMonth() -> float or int
        SetMonth(month)
        TransformToYear() -> Year
        TransformToDay() -> Day
        TransformToHour() -> Hour
        TransformToMinute() -> Minute
        TransformToSecond() -> Second
        AddTime(other) -> Month
        SubTime(other) -> Month
        MulTime(other) -> Month

    Properties:
        month
        _num (protected)
        _ratio (protected)
    """

    def __init__(self, month):

        """
        __init__(month) -> Month
        Define The 'Month' Object For You
        parameter month: The Month -> float or int
        """

        super().__init__()
        if type(month) != int and type(month) != float:
            raise TimeUnitError('Unexpected Month: {:s}'.format(str(month)))
        self._num = month
        self._ratio = 60 * 60 * 24 * 30

    def __str__(self):

        """
        __str__() -> str
        Get self._num
        """

        return str(self._num)

    def __repr__(self):

        """
        __repr__() -> str
        Get self._num
        """

        return str(self._num)

    def __bool__(self):

        """
        __bool__() -> bool
        Get Whether self._num Is 0
        """

        return bool(self._num)

    def __add__(self, other):

        """
        __add__(other) -> Month
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToMonth()

    def __iadd__(self, other):

        """
        __add__(other) -> Month
        Get Self And Other
        parameter other: self + other -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToMonth()

    def __sub__(self, other):

        """
        __sub__(other) -> Month
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToMonth()

    def __isub__(self, other):

        """
        __isub__(other) -> Month
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToMonth()

    def __mul__(self, other):

        """
        __mul__(other) -> Month
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Month(self._num * other)

    def __imul__(self, other):

        """
        __imul__(other) -> Month
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Month(self._num * other)

    def __gt__(self, other):

        """
        __gt__(other) -> bool
        Get Self > Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio > other._num * other._ratio

    def __ge__(self, other):

        """
        __ge__(other) -> bool
        Get Self >= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio >= other._num * other._ratio

    def __lt__(self, other):

        """
        __lt__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio < other._num * other._ratio

    def __le__(self, other):

        """
        __le__(other) -> bool
        Get Self <= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio <= other._num * other._ratio

    def __eq__(self, other):

        """
        __eq__(other) -> bool
        Get Self == Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio == other._num * other._ratio

    def __ne__(self, other):

        """
        __ne__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio != other._num * other._ratio

    def __call__(self, num):

        """
        __call__(num)
        Set self._num
        param num: The Number You Want To Set
        """

        if type(num) != int:
            raise TimeUnitError('Unexpected Year: {:s}'.format(str(num)))
        self._num = num

    def __int__(self):

        """
        __int__() -> int
        Get int(self._num)
        """

        return int(self._num)

    def __float__(self):

        """
        __float__() -> float
        Get float(self._num)
        """

        return float(self._num)

    def __pos__(self):

        """
        __pos__() -> float or int
        Get +self._num
        """

        return + self._num

    def __neg__(self):

        """
        __neg__() -> float or int
        Get -self._num
        """

        return - self._num

    def __ceil__(self):

        """
        __ceil__() -> int
        Get math.ceil(self._num)
        """

        return _math.ceil(self._num)

    def __floor__(self):

        """
        __floor__() -> int
        Get math.floor(self._num)
        """

        return _math.floor(self._num)

    def __trunc__(self):

        """
        __trunc__() -> int
        Get math.trunc(self._num)
        """

        return _math.trunc(self._num)

    @property
    def month(self):

        """
        Get The Month Of The Object
        """

        return self._num

    def GetMonth(self):

        """
        GetMonth() -> float or int
        Get The Month Of The Object
        """

        return self._num

    def SetMonth(self, month):

        """
        SetMonth(month)
        Set The Month Of The Object
        parameter month: The Month You Want To Set -> float or int
        """

        self._num = month

    def TransformToYear(self):

        """
        TransformToYear() -> Year
        Transform The Month To Year
        """

        return Year(self._num / 12)

    def TransformToDay(self):

        """
        TransformToDay() -> Day
        Transform The Month To Day
        """

        return Day(self._num * 30)

    def TransformToHour(self):

        """
        TransformToHour() -> Hour
        Transform The Month To Hour
        """

        return Hour(self._num * 30 * 24)

    def TransformToMinute(self):

        """
        TransformToMinute() -> Minute
        Transform The Month To Minute
        """

        return Minute(self._num * 30 * 24 * 60)

    def TransformToSecond(self):

        """
        TransformToSecond() -> Second
        Transform The Month To Second
        """

        return Second(self._num * 60 * 60 * 24 * 30)

    def AddTime(self, other):

        """
        AddTime(other) -> Month
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToMonth()

    def SubTime(self, other):

        """
        SubTime(other) -> Month
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToMonth()

    def MulTime(self, other):

        """
        MulTime(other) -> Month
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Month(self._num * other)


class Day(TimeUnit):

    """
    Define The 'Day' Object

    Methods:
        __init__(day) -> Day
        __str__() -> str
        __repr__() -> str
        __bool__() -> bool
        __add__(other) -> Day
        __iadd__(other) -> Day
        __sub__(other) -> Day
        __isub__(other) -> Day
        __mul__(other) -> Day
        __imul__(other) -> Day
        __gt__(other) -> bool
        __ge__(other) -> bool
        __lt__(other) -> bool
        __le__(other) -> bool
        __eq__(other) -> bool
        __ne__(other) -> bool
        __call__(num)
        __int__() -> int
        __float__() -> float
        __pos__() -> float or int
        __neg__() -> float or int
        __ceil__() -> int
        __floor__() -> int
        __trunc__() -> int
        GetDay() -> float or int
        SetDay(day)
        TransformToYear() -> Year
        TransformToMonth() -> Month
        TransformToHour() -> Hour
        TransformToMinute() -> Minute
        TransformToSecond() -> Second
        AddTime(other) -> Day
        SubTime(other) -> Day
        MulTime(other) -> Day
        ToDate() -> Date

    Properties:
        day
        _num (protected)
        _ratio (private)
    """

    def __init__(self, day):

        """
        __init__(day) -> Day
        Define The 'Day' Object For You
        parameter day: The Day -> float or int
        """

        super().__init__()
        if type(day) != float and type(day) != int:
            raise TimeUnitError('Unexpected Day: {:s}'.format(str(day)))
        self._num = day
        self._ratio = 60 * 60 * 24

    def __str__(self):

        """
        __str__() -> str
        Get self._num
        """

        return str(self._num)

    def __repr__(self):

        """
        __repr__() -> str
        Get self._num
        """

        return str(self._num)

    def __bool__(self):

        """
        __bool__() -> bool
        Get Whether self._num Is 0
        """

        return bool(self._num)

    def __add__(self, other):

        """
        __add__(other) -> Day
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToDay()

    def __iadd__(self, other):

        """
        __add__(other) -> Day
        Get Self And Other
        parameter other: self + other -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToDay()

    def __sub__(self, other):

        """
        __sub__(other) -> Day
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToDay()

    def __isub__(self, other):

        """
        __isub__(other) -> Day
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToDay()

    def __mul__(self, other):

        """
        __mul__(other) -> Day
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Day(self._num * other)

    def __imul__(self, other):

        """
        __imul__(other) -> Day
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Day(self._num * other)

    def __gt__(self, other):

        """
        __gt__(other) -> bool
        Get Self > Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio > other._num * other._ratio

    def __ge__(self, other):

        """
        __ge__(other) -> bool
        Get Self >= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio >= other._num * other._ratio

    def __lt__(self, other):

        """
        __lt__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio < other._num * other._ratio

    def __le__(self, other):

        """
        __le__(other) -> bool
        Get Self <= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio <= other._num * other._ratio

    def __eq__(self, other):

        """
        __eq__(other) -> bool
        Get Self == Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio == other._num * other._ratio

    def __ne__(self, other):

        """
        __ne__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio != other._num * other._ratio

    def __call__(self, num):

        """
        __call__(num)
        Set self._num
        param num: The Number You Want To Set
        """

        if type(num) != int:
            raise TimeUnitError('Unexpected Year: {:s}'.format(str(num)))
        self._num = num

    def __int__(self):

        """
        __int__() -> int
        Get int(self._num)
        """

        return int(self._num)

    def __float__(self):

        """
        __float__() -> float
        Get float(self._num)
        """

        return float(self._num)

    def __pos__(self):

        """
        __pos__() -> float or int
        Get +self._num
        """

        return + self._num

    def __neg__(self):

        """
        __neg__() -> float or int
        Get -self._num
        """

        return - self._num

    def __ceil__(self):

        """
        __ceil__() -> int
        Get math.ceil(self._num)
        """

        return _math.ceil(self._num)

    def __floor__(self):

        """
        __floor__() -> int
        Get math.floor(self._num)
        """

        return _math.floor(self._num)

    def __trunc__(self):

        """
        __trunc__() -> int
        Get math.trunc(self._num)
        """

        return _math.trunc(self._num)

    @property
    def day(self):

        """
        Get The Day Of The Object
        """

        return self._num

    def GetDay(self):

        """
        GetDay() -> float or int
        Get The Day Of The Object
        """

        return self._num

    def SetDay(self, day):

        """
        SetDay(day)
        Set The Object's Day
        parameter day: The Day You Want To Set -> float or int
        """

        if type(day) != int or type(day) != float:
            raise TimeUnitError('Unexpected Hour: {:s}'.format(str(day)))
        self._num = day

    def TransformToYear(self):

        """
        TransformToYear() -> Year
        Transform The Day To Year
        """

        return Year(self._num / 12 / 30)

    def TransformToMonth(self):

        """
        TransformToMonth() -> Month
        Transform The Day To Month
        """

        return Year(self._num / 30)

    def TransformToHour(self):

        """
        TransformToHour() -> Hour
        Transform The Day To Hour
        """

        return Hour(self._num * 24)

    def TransformToMinute(self):

        """
        TransformToMinute() -> Minute
        Transform The Day To Minute
        """

        return Minute(self._num * 24 * 60)

    def TransformToSecond(self):

        """
        TransformToSecond() -> Second
        Transform The Day To Second
        """

        return Second(self._num * 60 * 60 * 24)

    def AddTime(self, other):

        """
        AddTime(other) -> Day
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToDay()

    def SubTime(self, other):

        """
        SubTime(other) -> Day
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToDay()

    def MulTime(self, other):

        """
        MulTime(other) -> Day
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Day(self._num * other)

    def ToDate(self):

        """
        ToDate() -> Date
        Convert The Day Object To Date Object
        """

        sec = self.TransformToSecond().GetSecond()
        st = _time.localtime(sec)
        y = st.tm_year
        m = st.tm_mon
        d = st.tm_mday
        return Date(y, m, d)


class Hour(TimeUnit):

    """
    Define The 'Hour' Object

    Methods:
        __init__(hour) -> Hour
        __str__() -> str
        __repr__() -> str
        __bool__() -> bool
        __add__(other) -> Hour
        __iadd__(other) -> Hour
        __sub__(other) -> Hour
        __isub__(other) -> Hour
        __mul__(other) -> Hour
        __imul__(other) -> Hour
        __gt__(other) -> bool
        __ge__(other) -> bool
        __lt__(other) -> bool
        __le__(other) -> bool
        __eq__(other) -> bool
        __ne__(other) -> bool
        __call__(num)
        __int__() -> int
        __float__() -> float
        __pos__() -> float or int
        __neg__() -> float or int
        __ceil__() -> int
        __floor__() -> int
        __trunc__() -> int
        GetHour() -> float or int
        SetHour(hour)
        TransformToYear() -> Year
        TransformToMonth() -> Month
        TransformToDay() -> Day
        TransformToMinute() -> Minute
        TransformToSecond() -> Second
        AddTime(other) -> Hour
        SubTime(other) -> Hour
        MulTime(other) -> Hour

    Properties:
        hour
        _num (protected)
        _ratio (private)
    """

    def __init__(self, hour):

        """
        __init__(hour) -> Hour
        Define The 'Hour' Object For You
        parameter hour: The Hour -> float or int
        """

        super().__init__()
        if type(hour) != float and type(hour) != int:
            raise TimeUnitError('Unexpected Hour: {:s}'.format(str(hour)))
        self._num = hour
        self._ratio = 60 * 60

    def __str__(self):

        """
        __str__() -> str
        Get self._num
        """

        return str(self._num)

    def __repr__(self):

        """
        __repr__() -> str
        Get self._num
        """

        return str(self._num)

    def __bool__(self):

        """
        __bool__() -> bool
        Get Whether self._num Is 0
        """

        return bool(self._num)

    def __add__(self, other):

        """
        __add__(other) -> Hour
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToHour()

    def __iadd__(self, other):

        """
        __add__(other) -> Hour
        Get Self And Other
        parameter other: self + other -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToHour()

    def __sub__(self, other):

        """
        __sub__(other) -> Hour
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToHour()

    def __isub__(self, other):

        """
        __isub__(other) -> Hour
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToHour()

    def __mul__(self, other):

        """
        __mul__(other) -> Hour
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Hour(self._num * other)

    def __imul__(self, other):

        """
        __imul__(other) -> Hour
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Hour(self._num * other)

    def __gt__(self, other):

        """
        __gt__(other) -> bool
        Get Self > Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio > other._num * other._ratio

    def __ge__(self, other):

        """
        __ge__(other) -> bool
        Get Self >= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio >= other._num * other._ratio

    def __lt__(self, other):

        """
        __lt__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio < other._num * other._ratio

    def __le__(self, other):

        """
        __le__(other) -> bool
        Get Self <= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio <= other._num * other._ratio

    def __eq__(self, other):

        """
        __eq__(other) -> bool
        Get Self == Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio == other._num * other._ratio

    def __ne__(self, other):

        """
        __ne__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio != other._num * other._ratio

    def __call__(self, num):

        """
        __call__(num)
        Set self._num
        param num: The Number You Want To Set
        """

        if type(num) != int:
            raise TimeUnitError('Unexpected Year: {:s}'.format(str(num)))
        self._num = num

    def __int__(self):

        """
        __int__() -> int
        Get int(self._num)
        """

        return int(self._num)

    def __float__(self):

        """
        __float__() -> float
        Get float(self._num)
        """

        return float(self._num)

    def __pos__(self):

        """
        __pos__() -> float or int
        Get +self._num
        """

        return + self._num

    def __neg__(self):

        """
        __neg__() -> float or int
        Get -self._num
        """

        return - self._num

    def __ceil__(self):

        """
        __ceil__() -> int
        Get math.ceil(self._num)
        """

        return _math.ceil(self._num)

    def __floor__(self):

        """
        __floor__() -> int
        Get math.floor(self._num)
        """

        return _math.floor(self._num)

    def __trunc__(self):

        """
        __trunc__() -> int
        Get math.trunc(self._num)
        """

        return _math.trunc(self._num)

    @property
    def hour(self):

        """
        Get The Object's Hour
        """

        return self._num

    def GetHour(self):

        """
        GetHour() -> float or int
        Get The Object's Hour
        """

        return self._num

    def SetHour(self, hour):

        """
        SetHour(hour)
        Set The Object's Hour
        parameter hour: The Hour You Want To Set -> float or int
        """

        if type(hour) != int or type(hour) != float:
            raise TimeUnitError('Unexpected Hour: {:s}'.format(str(hour)))
        self._num = hour

    def TransformToYear(self):

        """
        TransformToYear() -> Year
        Transform The Hour To Year
        """

        return Year(self._num / 12 / 30 / 24)

    def TransformToMonth(self):

        """
        TransformToMonth() -> Month
        Transform The Hour To Month
        """

        return Month(self._num / 30 / 24)

    def TransformToDay(self):

        """
        TransformToDay() -> Day
        Transform The Hour To Day
        """

        return Day(self._num / 24)

    def TransformToMinute(self):

        """
        TransformToMinute() -> Minute
        Transform The Hour To Minute
        """

        return Minute(self._num * 60)

    def TransformToSecond(self):

        """
        TransformToSecond() -> Second
        Transform The Hour To Second
        """

        return Second(self._num * 60 * 60)

    def AddTime(self, other):

        """
        AddTime(other) -> Hour
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToHour()

    def SubTime(self, other):

        """
        SubTime(other) -> Hour
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToHour()

    def MulTime(self, other):

        """
        MulTime(other) -> Hour
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Hour(self._num * other)


class Minute(TimeUnit):

    """
    Define The 'Minute' Object

    Methods:
        __init__(minute) -> Minute
        __str__() -> str
        __repr__() -> str
        __bool__() -> bool
        __add__(other) -> Minute
        __iadd__(other) -> Minute
        __sub__(other) -> Minute
        __isub__(other) -> Minute
        __mul__(other) -> Minute
        __imul__(other) -> Minute
        __gt__(other) -> bool
        __ge__(other) -> bool
        __lt__(other) -> bool
        __le__(other) -> bool
        __eq__(other) -> bool
        __ne__(other) -> bool
        __call__(num)
        __int__() -> int
        __float__() -> float
        __pos__() -> float or int
        __neg__() -> float or int
        __ceil__() -> int
        __floor__() -> int
        __trunc__() -> int
        GetMinute() -> float or int
        SetMinute(minute)
        TransformToYear() -> Year
        TransformToMonth() -> Month
        TransformToDay() -> Day
        TransformToHour() -> Hour
        TransformToSecond() -> Second
        AddTime(other) -> Minute
        SubTime(other) -> Minute
        MulTime(other) -> Minute

    Properties:
        minute
        _num (protected)
        _ratio (private)
    """

    def __init__(self, minute):

        """
        __init__(minute) -> Minute
        Define The 'Minute' Object For You
        parameter minute: The Minute -> float or int
        """

        super().__init__()
        if type(minute) != float and type(minute) != int:
            raise TimeUnitError('Unexpected Minute: {:s}'.format(str(minute)))
        self._num = minute
        self._ratio = 60

    def __str__(self):

        """
        __str__() -> str
        Get self._num
        """

        return str(self._num)

    def __repr__(self):

        """
        __repr__() -> str
        Get self._num
        """

        return str(self._num)

    def __bool__(self):

        """
        __bool__() -> bool
        Get Whether self._num Is 0
        """

        return bool(self._num)

    def __add__(self, other):

        """
        __add__(other) -> Minute
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToMinute()

    def __iadd__(self, other):

        """
        __add__(other) -> Minute
        Get Self And Other
        parameter other: self + other -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToMinute()

    def __sub__(self, other):

        """
        __sub__(other) -> Minute
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToMinute()

    def __isub__(self, other):

        """
        __isub__(other) -> Minute
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToMinute()

    def __mul__(self, other):

        """
        __mul__(other) -> Minute
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Minute(self._num * other)

    def __imul__(self, other):

        """
        __imul__(other) -> Minute
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Minute(self._num * other)

    def __gt__(self, other):

        """
        __gt__(other) -> bool
        Get Self > Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio > other._num * other._ratio

    def __ge__(self, other):

        """
        __ge__(other) -> bool
        Get Self >= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio >= other._num * other._ratio

    def __lt__(self, other):

        """
        __lt__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio < other._num * other._ratio

    def __le__(self, other):

        """
        __le__(other) -> bool
        Get Self <= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio <= other._num * other._ratio

    def __eq__(self, other):

        """
        __eq__(other) -> bool
        Get Self == Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio == other._num * other._ratio

    def __ne__(self, other):

        """
        __ne__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio != other._num * other._ratio

    def __call__(self, num):

        """
        __call__(num)
        Set self._num
        param num: The Number You Want To Set
        """

        if type(num) != int:
            raise TimeUnitError('Unexpected Year: {:s}'.format(str(num)))
        self._num = num

    def __int__(self):

        """
        __int__() -> int
        Get int(self._num)
        """

        return int(self._num)

    def __float__(self):

        """
        __float__() -> float
        Get float(self._num)
        """

        return float(self._num)

    def __pos__(self):

        """
        __pos__() -> float or int
        Get +self._num
        """

        return + self._num

    def __neg__(self):

        """
        __neg__() -> float or int
        Get -self._num
        """

        return - self._num

    def __ceil__(self):

        """
        __ceil__() -> int
        Get math.ceil(self._num)
        """

        return _math.ceil(self._num)

    def __floor__(self):

        """
        __floor__() -> int
        Get math.floor(self._num)
        """

        return _math.floor(self._num)

    def __trunc__(self):

        """
        __trunc__() -> int
        Get math.trunc(self._num)
        """

        return _math.trunc(self._num)

    @property
    def minute(self):

        """
        Get The Object's Minute
        """

        return self._num

    def GetMinute(self):

        """
        GetMinute() -> float or int
        Get The Object's Minute
        """

        return self._num

    def SetMinute(self, minute):

        """
        SetMinute(minute)
        Set The Object's Minute
        parameter minute: The Minute You Want To Set -> float or int
        """

        if type(minute) != int or type(minute) != float:
            raise TimeUnitError('Unexpected Minute: {:s}'.format(str(minute)))
        self._num = minute

    def TransformToYear(self):

        """
        TransformToYear() -> Year
        Transform The Minute To Year
        """

        return Minute(self._num / 12 / 30 / 24 / 60)

    def TransformToMonth(self):

        """
        TransformToMonth() -> Month
        Transform The Minute To Month
        """

        return Month(self._num / 30 / 24 / 60)

    def TransformToDay(self):

        """
        TransformToDay() -> Day
        Transform The Minute To Day
        """

        return Day(self._num / 24 / 60)

    def TransformToHour(self):

        """
        TransformToHour() -> Hour
        Transform The Minute To Hour
        """

        return Hour(self._num / 60)

    def TransformToSecond(self):

        """
        TransformToSecond() -> Second
        Transform The Minute To Second
        """

        return Second(self._num * 60)

    def AddTime(self, other):

        """
        AddTime(other) -> Minute
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio).TransformToMinute()

    def SubTime(self, other):

        """
        SubTime(other) -> Minute
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio).TransformToMinute()

    def MulTime(self, other):

        """
        MulTime(other) -> Minute
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Minute(self._num * other)


class Second(TimeUnit):

    """
    Define The 'Second' Object

    Methods:
        __init__(second) -> Second
        __str__() -> str
        __repr__() -> str
        __bool__() -> bool
        __add__(other) -> Second
        __iadd__(other) -> Second
        __sub__(other) -> Second
        __isub__(other) -> Second
        __mul__(other) -> Second
        __imul__(other) -> Second
        __gt__(other) -> bool
        __ge__(other) -> bool
        __lt__(other) -> bool
        __le__(other) -> bool
        __eq__(other) -> bool
        __ne__(other) -> bool
        __call__(num)
        __int__() -> int
        __float__() -> float
        __pos__() -> float or int
        __neg__() -> float or int
        __ceil__() -> int
        __floor__() -> int
        __trunc__() -> int
        GetSecond() -> float or int
        SetSecond(second)
        TransformToYear() -> Year
        TransformToMonth() -> Month
        TransformToDay() -> Day
        TransformToHour() -> Hour
        TransformToMinute() -> Minute
        AddTime(other) -> Second
        SubTime(other) -> Second
        MulTime(other) -> Second

    Properties:
        second
        _num (protected)
        _ratio (private)
    """

    def __init__(self, second):

        """
        __init__(second) -> Second
        Define The 'Second' Object For You
        parameter second: The Second -> float or int
        """

        super().__init__()
        if type(second) != float and type(second) != int:
            raise TimeUnitError('Unexpected Second: {:s}'.format(str(second)))
        self._num = second
        self._ratio = 1

    def __str__(self):

        """
        __str__() -> str
        Get self._num
        """

        return str(self._num)

    def __repr__(self):

        """
        __repr__() -> str
        Get self._num
        """

        return str(self._num)

    def __bool__(self):

        """
        __bool__() -> bool
        Get Whether self._num Is 0
        """

        return bool(self._num)

    def __add__(self, other):

        """
        __add__(other) -> Second
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio)

    def __iadd__(self, other):

        """
        __add__(other) -> Second
        Get Self And Other
        parameter other: self + other -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio)

    def __sub__(self, other):

        """
        __sub__(other) -> Second
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio)

    def __isub__(self, other):

        """
        __isub__(other) -> Second
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio)

    def __mul__(self, other):

        """
        __mul__(other) -> Second
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * other)

    def __imul__(self, other):

        """
        __imul__(other) -> Second
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * other)

    def __gt__(self, other):

        """
        __gt__(other) -> bool
        Get Self > Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio > other._num * other._ratio

    def __ge__(self, other):

        """
        __ge__(other) -> bool
        Get Self >= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio >= other._num * other._ratio

    def __lt__(self, other):

        """
        __lt__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio < other._num * other._ratio

    def __le__(self, other):

        """
        __le__(other) -> bool
        Get Self <= Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio <= other._num * other._ratio

    def __eq__(self, other):

        """
        __eq__(other) -> bool
        Get Self == Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio == other._num * other._ratio

    def __ne__(self, other):

        """
        __ne__(other) -> bool
        Get Self < Other
        parameter other: The Other Value -> Year Or Month Or Day Or Hour Or Minute Or Second
        """

        return self._num * self._ratio != other._num * other._ratio

    def __call__(self, num):

        """
        __call__(num)
        Set self._num
        param num: The Number You Want To Set
        """

        if type(num) != int:
            raise TimeUnitError('Unexpected Year: {:s}'.format(str(num)))
        self._num = num

    def __int__(self):

        """
        __int__() -> int
        Get int(self._num)
        """

        return int(self._num)

    def __float__(self):

        """
        __float__() -> float
        Get float(self._num)
        """

        return float(self._num)

    def __pos__(self):

        """
        __pos__() -> float or int
        Get +self._num
        """

        return + self._num

    def __neg__(self):

        """
        __neg__() -> float or int
        Get -self._num
        """

        return - self._num

    def __ceil__(self):

        """
        __ceil__() -> int
        Get math.ceil(self._num)
        """

        return _math.ceil(self._num)

    def __floor__(self):

        """
        __floor__() -> int
        Get math.floor(self._num)
        """

        return _math.floor(self._num)

    def __trunc__(self):

        """
        __trunc__() -> int
        Get math.trunc(self._num)
        """

        return _math.trunc(self._num)

    @property
    def second(self):

        """
        Get The Object's Second
        """

        return self._num

    def GetSecond(self):

        """
        GetSecond() -> float or int
        Get The Object's Second
        """

        return self._num

    def SetSecond(self, second):

        """
        SetSecond(second)
        Set The Object's Second
        parameter second: The Second You Want To Set -> float or int
        """

        if type(second) != int or type(second) != float:
            raise TimeUnitError('Unexpected Second: {:s}'.format(str(second)))
        self._num = second

    def TransformToYear(self):

        """
        TransformToYear() -> Year
        Transform The Second To Year
        """

        return Minute(self._num / 12 / 30 / 24 / 3600)

    def TransformToMonth(self):

        """
        TransformToMonth() -> Month
        Transform The Second To Month
        """

        return Month(self._num / 30 / 24 / 3600)

    def TransformToDay(self):

        """
        TransformToDay() -> Day
        Transform The Second To Day
        """

        return Day(self._num / 24 / 3600)

    def TransformToHour(self):

        """
        TransformToHour() -> Hour
        Transform The Second To Hour
        """

        return Hour(self._num / 3600)

    def TransformToMinute(self):

        """
        TransformToMinute() -> Minute
        Transform The Second To Minute
        """

        return Minute(self._num / 60)

    def AddTime(self, other):

        """
        AddTime(other) -> Second
        Get Self And Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * self._ratio + other._num * other._ratio)

    def SubTime(self, other):

        """
        SubTime(other) -> Second
        Get Self Subtract Other
        parameter other: self + other
        """

        if not isinstance(other, TimeUnit):
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        if self._num * self._ratio - other._num * other._ratio < 0:
            raise TimeUnitError

        return Second(self._num * self._ratio - other._num * other._ratio)

    def MulTime(self, other):

        """
        MulTime(other) -> Second
        Get Self Multiply Other
        parameter other: The Int Object -> int
        """

        if type(other) != int:
            raise TimeUnitError('Unexpected Operation Or Type: {:s}'.format(str(type(other))))

        return Second(self._num * other)


class TimeStamp:

    """
    A TimeStamp Object

    Methods:
        __init__(time_stamp_float_number) -> TimeStamp
        __str__() -> str
        __repr__() -> str
        __add__(other) -> TimeStamp
        __sub__(other) -> TimeStamp
        __mul__(other) -> TimeStamp
        __truediv__(other) -> TimeStamp
        __floordiv__(other) -> TimeStamp
        __mod__(other) -> TimeStamp
        __pow__(other) -> TimeStamp
        __lshift__(other) -> TimeStamp
        __rshift__(other) -> TimeStamp
        __iadd__(other) -> TimeStamp
        __isub__(other) -> TimeStamp
        __imul__(other) -> TimeStamp
        __itruediv__(other) -> TimeStamp
        __ifloordiv__(other) -> TimeStamp
        __imod__(other) -> TimeStamp
        __ipow__(other) -> TimeStamp
        __ilshift__(other) -> TimeStamp
        __irshift__(other) -> TimeStamp
        __divmod__(other) -> TimeStamp
        __lt__(other) -> bool
        __le__(other) -> bool
        __gt__(other) -> bool
        __ge__(other) -> bool
        __eq__(other) -> bool
        __ne__(other) -> bool
        __abs__() -> int
        __int__() -> int
        __float__() -> float
        __round__(digit=None) -> int
        __trunc__() -> int
        __floor__() -> int
        __ceil__() -> int
        __pos__() -> TimeStamp
        __neg__() -> TimeStamp
        GetTimeStamp() -> float
        SetTimeStamp(time_stamp_float_number)
        Add(other) -> TimeStamp
        Subtract(other) -> TimeStamp
        Multiply(other) -> TimeStamp
        ToDateTime() -> DateTime
        Clone() -> TimeStamp
        Now() -> TimeStamp
        ToStructTime() -> time.struct_time
        ToDate() -> Date

    Properties:
        time_stamp
        _time_stamp (protected)
    """

    def __init__(self, time_stamp_float_number=None):

        """
        __init__(time_stamp_float_number) -> TimeStamp
        Create A TimeStamp Object For You
        parameter time_stamp_float_number: A Float Number Which Is A TimeStamp -> float or None
        """

        if time_stamp_float_number is None:
            self._time_stamp = _time.time()
        else:
            if not type(time_stamp_float_number) == float:
                raise TimeStampError('Unexpected parameter: time_stamp_float_number.')
            self._time_stamp = time_stamp_float_number

    def __str__(self):

        """
        __str__() -> str
        Get str(self.time_stamp)
        """

        return str(self._time_stamp)

    def __repr__(self):

        """
        __repr__() -> str
        Get str(self.time_stamp)
        """

        return str(self._time_stamp)

    def __add__(self, other):

        """
        __add__(other) -> TimeStamp
        Add Self And Other
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != TimeStamp:
            raise TimeStampError
        return TimeStamp(self._time_stamp + other._time_stamp)

    def __sub__(self, other):

        """
        __sub__(other) -> TimeStamp
        Get Self Subtract Other
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != TimeStamp:
            raise TimeStampError
        if other._time_stamp > self._time_stamp:
            raise TimeStampError
        return TimeStamp(self._time_stamp - other._time_stamp)

    def __mul__(self, other):

        """
        __mul__(other) -> TimeStamp
        Get Self Multiply Other
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp * other)

    def __truediv__(self, other):

        """
        __truediv__(other) -> TimeStamp
        Get Self / Other
        parameter other: An int Object -> int
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp / other)

    def __floordiv__(self, other):

        """
        __floordiv__(other) -> TimeStamp
        Get Self // Other
        parameter other: An int Object -> int
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp // other)

    def __mod__(self, other):

        """
        __mod__(other) -> TimeStamp
        Get Self % Other
        parameter other: An int Object -> int
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp % other)

    def __pow__(self, power):

        """
        __pow__(power) -> TimeStamp
        Get self ** power
        parameter power: An int Object -> int
        """

        if type(power) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp ** power)

    def __lshift__(self, other):

        """
        __lshift__(other) -> TimeStamp
        Get Self << Other
        parameter other: An int Object
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp << other)

    def __rshift__(self, other):

        """
        __rshift__(other) -> TimeStamp
        Get Self >> Other
        parameter other: An int Object
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp >> other)

    def __iadd__(self, other):

        """
        __add__(other) -> TimeStamp
        Add Self And Other
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != TimeStamp:
            raise TimeStampError
        return TimeStamp(self._time_stamp + other._time_stamp)

    def __isub__(self, other):

        """
        __sub__(other) -> TimeStamp
        Get Self Subtract Other
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != TimeStamp:
            raise TimeStampError
        if other._time_stamp > self._time_stamp:
            raise TimeStampError
        return TimeStamp(self._time_stamp - other._time_stamp)

    def __imul__(self, other):

        """
        __mul__(other) -> TimeStamp
        Get Self Multiply Other
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp * other)

    def __itruediv__(self, other):

        """
        __itruediv__(other) -> TimeStamp
        Get Self /= Other
        parameter other: An int Object -> int
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp / other)

    def __ifloordiv__(self, other):

        """
        __ifloordiv__(other) -> TimeStamp
        Get Self //= Other
        parameter other: An int Object -> int
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp // other)

    def __imod__(self, other):

        """
        __imod__(other) -> TimeStamp
        Get Self %= Other
        parameter other: An int Object -> int
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp % other)

    def __ipow__(self, power):

        """
        __ipow__(power) -> TimeStamp
        Get self **= power
        parameter power: An int Object -> int
        """

        if type(power) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp ** power)

    def __ilshift__(self, other):

        """
        __ilshift__(other) -> TimeStamp
        Get Self <<= Other
        parameter other: An int Object
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp << other)

    def __irshift__(self, other):

        """
        __irshift__(other) -> TimeStamp
        Get Self >>= Other
        parameter other: An int Object
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp >> other)

    def __divmod__(self, other):

        """
        __divmod__(other) -> TimeStamp
        Get divmod(self, other)
        parameter other: An int Object -> int
        """

        if type(other) != int:
            raise TimeStampError
        return (TimeStamp(self._time_stamp // other), TimeStamp(self._time_stamp % other))

    def __lt__(self, other):

        """
        __lt__(other) -> bool
        Get self._time_stamp < other._time_stamp
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != TimeStamp:
            raise TimeStampError
        return self._time_stamp < other._time_stamp

    def __le__(self, other):

        """
        __le__(other) -> bool
        Get self._time_stamp <= other._time_stamp
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != TimeStamp:
            raise TimeStampError
        return self._time_stamp <= other._time_stamp

    def __gt__(self, other):

        """
        __gt__(other) -> bool
        Get self._time_stamp > other._time_stamp
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != TimeStamp:
            raise TimeStampError
        return self._time_stamp > other._time_stamp

    def __ge__(self, other):

        """
        __ge__(other) -> bool
        Get self._time_stamp >= other._time_stamp
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != TimeStamp:
            raise TimeStampError
        return self._time_stamp >= other._time_stamp

    def __eq__(self, other):

        """
        __eq__(other) -> bool
        Get self._time_stamp == other._time_stamp
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != TimeStamp:
            raise TimeStampError
        return self._time_stamp == other._time_stamp

    def __ne__(self, other):

        """
        __ne__(other) -> bool
        Get self._time_stamp != other._time_stamp
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != TimeStamp:
            raise TimeStampError
        return self._time_stamp != other._time_stamp

    def __abs__(self):

        """
        __abs__() -> int
        Get abs(self._time_stamp)
        """

        return abs(self._time_stamp)

    def __int__(self):

        """
        __int__() -> int
        Get int(self._time_stamp)
        """

        return int(self._time_stamp)

    def __float__(self):

        """
        __float__() -> float
        Get float(self._time_stamp)
        """

        return float(self._time_stamp)

    def __round__(self, digit=None):

        """
        __round__(digit=None) -> int
        Get round(self._time_stamp)
        parameter digit: Digit -> int
        """

        return round(self._time_stamp, digit)

    def __trunc__(self):

        """
        __trunc__() -> int
        Get math.trunc(self._time_stamp)
        """

        return _math.trunc(self._time_stamp)

    def __floor__(self):

        """
        __floor__() -> int
        Get math.floor(self._time_stamp)
        """

        return _math.floor(self._time_stamp)

    def __ceil__(self):

        """
        __ceil__() -> int
        Get math.ceil(self._time_stamp)
        """

        return _math.ceil(self._time_stamp)

    def __pos__(self):

        """
        __pos__() -> TimeStamp
        Get + Self
        """

        return TimeStamp(+ self._time_stamp)

    def __neg__(self):

        """
        __neg__() -> TimeStamp
        Get - Self
        """

        return TimeStamp(- self._time_stamp)

    @property
    def time_stamp(self):

        """
        Get self._time_stamp
        """

        return self._time_stamp

    def GetTimeStamp(self):

        """
        GetTimeStamp() -> float
        Getself._time_stamp
        """

        return self._time_stamp

    def SetTimeStamp(self, time_stamp_float_number):

        """
        SetTimeStamp(time_stamp_float_number)
        Set self._time_stamp
        parameter time_stamp_float_number: A Float Number Which Is A TimeStamp Number -. float
        """

        if time_stamp_float_number is None:
            self._time_stamp = _time.time()
        else:
            if (not type(time_stamp_float_number) == float) or time_stamp_float_number < 0:
                raise TimeStampError('Unexpected parameter: time_stamp_float_number.')
            self._time_stamp = time_stamp_float_number

    def Add(self, other):

        """
        Add(other) -> TimeStamp
        Add Self And Other
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != TimeStamp:
            raise TimeStampError
        return TimeStamp(self._time_stamp + other._time_stamp)

    def Subtract(self, other):

        """
        Subtract(other) -> TimeStamp
        Get Self Subtract Other
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != TimeStamp:
            raise TimeStampError
        if other._time_stamp > self._time_stamp:
            raise TimeStampError
        return TimeStamp(self._time_stamp - other._time_stamp)

    def Multiply(self, other):

        """
        Multiply(other) -> TimeStamp
        Get Self Multiply Other
        parameter other: A TimeStamp Object -> TimeStamp
        """

        if type(other) != int:
            raise TimeStampError
        return TimeStamp(self._time_stamp * other)

    def ToDateTime(self):

        """
        ToDateTime() -> DateTime
        Transform The TimeStamp Object To DateTime Object
        """

        year = _time.strftime(
            '%Y', _time.localtime(
                self._time_stamp
            )
        )
        month = _time.strftime(
            '%m', _time.localtime(
                self._time_stamp
            )
        )
        day = _time.strftime(
            '%d', _time.localtime(
                self._time_stamp
            )
        )
        hour = _time.strftime(
            '%H', _time.localtime(
                self._time_stamp
            )
        )
        minute = _time.strftime(
            '%M', _time.localtime(
                self._time_stamp
            )
        )
        second = _time.strftime(
            '%S', _time.localtime(
                self._time_stamp
            )
        )
        str_ts = str(
            self._time_stamp
        )
        index = str_ts.find(
            '.'
        )
        zs = str_ts[
            index + 1
        ]
        zzs = str_ts[
            index + 2
        ]
        zzzs = str_ts[
            index + 3
        ]
        year = int(
            year
        )
        month = int(
            month
        )
        day = int(
            day
        )
        hour = int(
            hour
        )
        minute = int(
            minute
        )
        second = int(
            second
        )
        zs = int(
            zs
        )
        zzs = int(
            zzs
        )
        zzzs = int(
            zzzs
        )
        datetime = DateTime(
            year,
            month,
            day,
            hour,
            minute,
            second,
            zs,
            zzs,
            zzzs
        )
        return datetime

    def Clone(self):

        """
        Clone() -> TimeStamp
        Clone Self
        """

        return self

    @classmethod
    def Now(cls):

        """
        Now() -> TimeStamp
        Get Time Stamp Now
        """

        tsfloat = _time.time()
        tsobj = cls(tsfloat)
        return tsobj

    def ToStructTime(self):

        """
        ToStructTime() -> time.struct_time
        Convert The TimeStamp Object To time.struct_time Object
        """

        st = _time.localtime(self._time_stamp)
        return st

    def ToDate(self):

        """
        ToDate() -> Date
        Convert The TimeStamp Object To Date Object
        """

        st = self.ToStructTime()
        year = st.tm_year
        month = st.tm_mon
        day = st.tm_mday
        return Date(year, month, day)


class Date:

    """
    Define The Date Class.
    
    Methods:
        __init__(year, month, day) -> Date
        __add__(other) -> Date
        __iadd__(other) -> Date
        __str__() -> str
        __repr__() -> str
        __int__() -> int
        __float__() -> float
        __lt__(other) -> bool
        __le__(other) -> bool
        __gt__(other) -> bool
        __le__(other) -> bool
        __eq__(other) -> bool
        __ne__(other) -> bool
        GetYear() -> int
        GetMonth() -> int
        GetDay() -> int
        GetWeekDay() -> int (range[0, 6])
        GetYearDay() -> int (range[1, 366])
        SetYear(year)
        SetMonth(month)
        SetDay(day)
        IsLeapYear() -> bool
        ToTimeStamp() -> TimeStamp
        Clone() -> Date
        Now() -> Date
        ToDay() -> Day
        Add(other) -> Date
        GetNextMonthDate() -> Date
        GetNextYearDate() -> Date
        GetNextDayDate() -> Date
        GetPreviousMonthDate() -> Date
        GetPreviousDayDate() -> Date
        GetPreviousYearDate() -> Date
        
    Properties:
        year
        month
        day
        _day (protected)
        _month (protected)
        _year (protected)
        max_day
        max_month
        min_day
        min_month
    """

    # define class attribute
    min_month = 1
    max_month = 12
    min_day = 1
    max_day = 31

    def __init__(self, year: int, month: int, day: int):

        """
        __init__(year, month, day) -> Date
        Initial The Date
        parameter year: The Year -> int
        parameter month: The Month -> int
        parameter day: The Day -> int
        """

        day_of_month_c = day_of_month

        if type(year) != int or type(month) != int or type(day) != int:
            raise DateError('Unexpected Argument.')

        if not Date.min_month <= month <= Date.max_month:
            raise DateError('Unexpected Argument: month.')

        if not Date.min_day <= day <= Date.max_day:
            raise DateError('Unexpected Argument: day.')

        if month == 2:
            if Date(year, 1, 1).IsLeapYear():
                day_of_month_c[1] = 29

        if day_of_month_c[month - 1] < day:
            raise DateError('Argument day Should Be 1-{0:d}'.format(day_of_month_c[month - 1]))

        self._year = year
        self._month = month
        self._day = day

    def __add__(self, other):

        """
        __add__(other) -> Date
        Get Self And Other
        parameter other: The Other Date -> Date
        """

        if not isinstance(other, Date):
            raise DateError

        ad = 0
        ad += self._day
        ad += other._day
        ad += DaysBeforeMonth(self._year, self._month)
        ad += DaysBeforeMonth(other._year, other._month)
        ad += DaysBeforeYear(self._year - 1969)
        ad += DaysBeforeYear(other._year - 1969)
        return Day(ad).ToDate()

    def __iadd__(self, other):

        """
        __iadd__(other) -> Date
        Get Self And Other
        parameter other: The Other Date -> Date
        """

        if not isinstance(other, Date):
            raise DateError

        ad = 0
        ad += self._day
        ad += other._day
        ad += DaysBeforeMonth(self._year, self._month)
        ad += DaysBeforeMonth(other._year, other._month)
        ad += DaysBeforeYear(self._year - 1969)
        ad += DaysBeforeYear(other._year - 1969)
        return Day(ad).ToDate()

    def __str__(self):

        """
        __str__() -> str
        Get The Tuple String Of Date
        """

        return str((self._year, self._month, self._day))

    def __repr__(self):

        """
        __repr__() -> str
        Get The Tuple String Of Date
        """

        return str((self._year, self._month, self._day))

    def __int__(self):

        """
        __int__() -> int
        Get The Days Of Date
        """

        day = self._day
        day += self._year
        day += DaysBeforeMonth(self._year, self._month)
        return day

    def __float__(self):

        """
        __int__() -> int
        Get The Days Of Date
        """

        day = self._day
        day += self._year
        day += DaysBeforeMonth(self._year, self._month)
        day = float(day)
        return day

    def __lt__(self, other):

        """
        __lt__(other) -> bool
        Get Self < Value
        parameter other: The Other Date -> Date
        """

        if not isinstance(other, Date):
            raise DateError

        if self._year < other._year:
            return True
        elif self._month < other._month:
            return True
        elif self._day < other._day:
            return True
        return False

    def __le__(self, other):

        """
        __le__(other) -> bool
        Get Self <= Value
        parameter other: The Other Date -> Date
        """

        if not isinstance(other, Date):
            raise DateError

        if self._year <= other._year:
            return True
        elif self._month <= other._month:
            return True
        elif self._day <= other._day:
            return True
        return False

    def __gt__(self, other):

        """
        __gt__(other) -> bool
        Get Self > Value
        parameter other: The Other Date -> Date
        """

        if not isinstance(other, Date):
            raise DateError

        if self._year > other._year:
            return True
        elif self._month > other._month:
            return True
        elif self._day > other._day:
            return True
        return False

    def __ge__(self, other):

        """
        __ge__(other) -> bool
        Get Self >= Value
        parameter other: The Other Date -> Date
        """

        if not isinstance(other, Date):
            raise DateError

        if self._year >= other._year:
            return True
        elif self._month >= other._month:
            return True
        elif self._day >= other._day:
            return True
        return False

    def __eq__(self, other):

        """
        __eq__(other) -> bool
        Get Self == Value
        parameter other: The Other Date -> Date
        """

        if not isinstance(other, Date):
            raise DateError

        if self._year == other._year and self._month == other._month and self._day == other._day:
            return True
        return False

    def __ne__(self, other):

        """
        __ne__(other) -> bool
        Get Self != Value
        parameter other: The Other Date -> Date
        """

        if not isinstance(other, Date):
            raise DateError

        if self._year != other._year:
            return True
        elif self._month != other._month:
            return True
        elif self._day != other._day:
            return True
        return False

    @property
    def year(self):

        """
        Get The Year Of Date
        """

        return self._year

    @property
    def month(self):

        """
        Get The Month Of Date
        """

        return self._month

    @property
    def day(self):

        """
        Get The Day Of Date
        """

        return self._day

    def GetYear(self):

        """
        GetYear() -> int
        Get The Year Of Date
        """

        return self._year

    def GetMonth(self):

        """
        GetMonth() -> int
        Get The Month Of Date
        """

        return self._month

    def GetDay(self):

        """
        GetDay() -> int
        Get The Day Of Date
        """

        return self._day

    def GetWeekday(self):

        """
        GetWeekDay() -> int (range[0, 6])
        Get The Weekday Of Date
        """

        tsf = self.ToTimeStamp().GetTimeStamp()
        st = _time.localtime(tsf)
        return st.tm_wday

    def GetYearDay(self):

        """
        GetYearDay() -> int (range[1, 366])
        Get The Year Day Of Date
        """

        tsf = self.ToTimeStamp().GetTimeStamp()
        st = _time.localtime(tsf)
        return st.tm_mday

    def SetYear(self, year: int):

        """
        SetYear(year)
        Set The Year Of The Date
        parameter year: The Year -> int
        """

        if not type(year) == int:
            raise DateError

        e = str(year)

        if not Date(year, 1, 1).IsLeapYear():
            if self._month == 2 and self._day == 29:
                raise DateError(e)

        self._year = year

    def SetMonth(self, month: int):

        """
        SetMonth(month)
        Set The Month Of The Date
        parameter month: The Month -> int
        """

        if not type(month) == int:
            raise DateError

        e = str(month)

        if Date.min_month <= month <= Date.max_month:
            raise DateError(e)

        if month == 4 or month == 6 or month == 9 or month == 11:
            if self._day > 30:
                raise DateError(e)

        if month == 2:
            if Date(self._year, 1, 1).IsLeapYear():
                if self._day > 29:
                    raise DateError(e)
            else:
                if self._day > 28:
                    raise DateError(e)

        self._month = month

    def SetDay(self, day: int):

        """
        SetDay(day)
        Set The Day Of The Date
        parameter day: The Day -> int
        """

        if not type(day) == int:
            raise DateError

        e = str(day)

        if not Date.min_day <= day <= Date.max_day:
            raise DateError(e)

        if self._month == 4 or self._month == 6 or self._month == 9 or self._month == 11:
            if day > 30:
                raise DateError(e)

        if self._month == 2:
            if Date(self._year, 1, 1).IsLeapYear():
                if day > 29:
                    raise DateError(e)
            else:
                if day > 28:
                    raise DateError(e)

        self._day = day

    def IsLeapYear(self):

        """
        IsLeapYear() -> bool
        Acquire Whether The Year Of Date Is A Leap Year
        """

        r1 = self._year % 4 == 0
        r2 = self._year % 100 == 0
        r3 = self._year % 400 == 0
        if r2:
            return r3
        return r1

    def ToTimeStamp(self):

        """
        ToTimeStamp() -> TimeStamp
        Convert The Date Object To TimeStamp Object
        """

        if self._year < 1970:
            raise DateError

        tsf = 0
        r = 0
        if self.IsLeapYear():
            r = 1
        tsf += (self._year - 1970) * 60 * 60 * 24 * (365 + r)
        tsf += DaysBeforeMonth(self._year, self._month).GetDay() * 60 * 60 * 24
        tsf += (self._day - 1) * 60 * 60 * 24
        tso = TimeStamp(tsf)
        return tso

    def Clone(self):

        """
        Clone() -> Date
        Clone Self
        """

        return self

    @classmethod
    def Now(cls):

        """
        Now() -> Date
        Get The Date Now
        """

        st = _time.localtime()
        y = st.tm_year
        m = st.tm_mon
        d = st.tm_mday
        return cls(y, m, d)

    def ToDay(self):

        """
        ToDay() -> Day
        Convert The Date Object To Day Object
        """

        day = 0
        r = 0
        if self.IsLeapYear():
            r = 1
        day += self._year * (365 + r)
        day += DaysBeforeMonth(self._year, self._month).GetDay()
        day += self._day
        do = Day(day)
        return do

    def Add(self, other):

        """
        Add(other) -> Date
        Get Self And Other
        parameter other: The Other Date -> Date
        """

        if not isinstance(other, Date):
            raise DateError

        ad = 0
        ad += self._day
        ad += other._day
        ad += DaysBeforeMonth(self._year, self._month)
        ad += DaysBeforeMonth(other._year, other._month)
        ad += DaysBeforeYear(self._year - 1969)
        ad += DaysBeforeYear(other._year - 1969)
        return Day(ad).ToDate()

    def GetNextMonthDate(self):

        """
        GetNextMonthDate() -> Date
        Get The Next Month Of The Date
        """

        y = self._year
        m = self._month
        d = self._day
        if m == 12:
            y += 1
            m = 1
        else:
            m += 1
        if m == 4 or m == 6 or m == 9 or m == 11:
            if d == 31:
                d = 30
        elif m == 2:
            if Date(y, 1, 1).IsLeapYear():
                if d > 29:
                    d = 29
            else:
                if d > 28:
                    d = 28
        return Date(y, m, d)

    def GetNextYearDate(self):

        """
        GetNextYearDate() -> Date
        Get The Next Year Of The Date
        """

        y = self._year
        m = self._month
        d = self._day
        y += 1
        if m == 2 and d == 29:
            d = 28
        return Date(y, m, d)

    def GetNextDayDate(self):

        """
        GetNextDayDate() -> Date
        Get The Next Day Of The Date
        """

        y = self._year
        m = self._month
        d = self._day
        d += 1
        if m == 4 or m == 6 or m == 9 or m == 11:
            if d == 31:
                d = 1
                m += 1
        else:
            if m != 2:
                if d == 32:
                    d = 1
                    m += 1
            else:
                if Date(y, 1, 1).IsLeapYear():
                    if d == 30:
                        m += 1
                        d = 1
                else:
                    if d == 29:
                        m += 1
                        d = 1
        if m == 13:
            y += 1
            m = 1
        return Date(y, m, d)

    def GetPreviousMonthDate(self):

        """
        GetPreviousMonthDate() -> Date
        Get The Previous Month Of The Date
        """

        y = self._year
        m = self._month
        d = self._day
        if m == 1:
            m = 12
            y -= 1
            if y < 0:
                raise DateError
        else:
            m -= 1
            if m == 4 or m == 6 or m == 9 or m == 11:
                if d == 31:
                    d = 30
            elif m == 2:
                if Date(y, 1, 1).IsLeapYear():
                    if d > 29:
                        d = 29
                else:
                    if d > 28:
                        d = 28

        return Date(y, m, d)

    def GetPreviousDayDate(self):

        """
        GetPreviousDayDate() -> Date
        Get The Previous Day Of The Date
        """

        d = 0
        d += self._day
        d += DaysBeforeMonth(self._year, self._month).GetDay()
        d += DaysBeforeYear(self._year - 1969).GetDay()
        d -= 2
        if d < 0:
            raise DateError
        day_obj = Day(d)
        return day_obj.ToDate()

    def GetPreviousYearDate(self):

        """
        GetPreviousYearDate() -> Date
        Get The Previous Year Of The Date
        """

        y = self._year
        m = self._month
        d = self._day
        if y == 0:
            raise DateError

        y -= 1
        if Date((y + 1), 1, 1).IsLeapYear():
            if m == 2 and d == 29:
                d = 28
        return Date(y, m, d)


class Calendar:

    """
    Define The Calendar Object
    
    Methods:
        __init__(first_weekday=0, is_leap_year=False) -> Calendar
        __str__() -> str
        __repr__() -> str
        GetFirstWeekday() -> int (range[0, 6], Monday Is 0)
        GetIsLeapYear() -> bool
        SetFirstWeekDay(first_weekday)
        SetIsLeapYear(is_leap_year)
        GetWeekdayByYearDay(year_day=0) -> int (range[0, 6], Monday Is 0)
        GetWeekdayByMonthAndDay(month=1, day=1) -> int (range[0, 6], Monday Is 0)
        GetCalendarThisYear() -> Calendar
        GetCalendarByYear(year) -> Calendar

    Properties:
        first_weekday
        is_leap_year
        _first_weekday
        _is_leap_year
        max_first_weekday
        min_first_weekday
    """

    # Define class attribute
    min_first_weekday = 0
    max_first_weekday = 6

    def __init__(self, first_weekday=0, is_leap_year=False):

        """
        __init__(first_weekday=0, is_leap_year=False) -> Calendar
        Define The Calendar Class
        parameter first_weekday: The First Weekday Of The Calendar -> int (range[0, 6], Monday Is 0)
        parameter is_leap_year: The Year Of The Calendar Is Leap Year If It's True -> bool
        """

        if type(first_weekday) != int:
            raise CalendarError

        if not Calendar.min_first_weekday <= first_weekday <= Calendar.max_first_weekday:
            raise CalendarError

        self._first_weekday = first_weekday
        self._is_leap_year = bool(is_leap_year)

    def __str__(self):

        """
        __str__() -> str
        Get str(self._first_weekday)
        """

        return str(self._first_weekday)

    def __repr__(self):

        """
        __str__() -> str
        Get str(self._first_weekday)
        """

        return str(self._first_weekday)

    @property
    def first_weekday(self):

        """
        Get The First Weekday Of Calendar
        """

        return self._first_weekday

    @property
    def is_leap_year(self):

        """
        Get self._is_leap_year
        """

        return self._is_leap_year

    def GetFirstWeekday(self):

        """
        GetFirstWeekday() -> int (range[0, 6], Monday Is 0)
        Get The First Weekday Of Calendar
        """

        return self._first_weekday

    def GetIsLeapYear(self):

        """
        GetIsLeapYear() -> bool
        Get self._is_leap_year
        """

        return self._is_leap_year

    def SetFirstWeekday(self, first_weekday: int):

        """
        SetFirstWeekDay(first_weekday)
        Set The First Weekday Of Calendar
        parameter first_weekday: The First Weekday -> int (range[0, 6], Monday Is 0)
        """

        if type(first_weekday) != int:
            raise CalendarError

        if not Calendar.min_first_weekday <= first_weekday <= Calendar.max_first_weekday:
            raise CalendarError

        self._first_weekday = first_weekday

    def SetIsLeapYear(self, is_leap_year):

        """
        SetIsLeapYear(is_leap_year)
        Set The Attribute Of Calendar: is_leap_year
        parameter is_leap_year: The Year Of The Calendar Is Leap Year If It's True -> bool
        """

        self._is_leap_year = bool(is_leap_year)

    def GetWeekdayByYearDay(self, year_day=1):

        """
        GetWeekdayByYearDay(year_day=0) -> int (range[0, 6], Monday Is 0)
        Get The Weekday Of Calendar By Year Day
        parameter year_day: Day Of Year -> int (range[1, 366])
        """

        if not type(year_day) == int:
            raise CalendarError

        if self._is_leap_year:
            if not 1 <= year_day <= 366:
                raise CalendarError
        else:
            if not 1 <= year_day <= 365:
                raise CalendarError

        yd = year_day
        yd %= 7
        yd += self._first_weekday
        yd %= 7
        return yd

    def GetWeekdayByMonthAndDay(self, month=1, month_day=1):

        """
        GetWeekdayByMonthAndDay(month=1, day=1) -> int (range[0, 6], Monday Is 0)
        Get The Weekday Of Calendar My Month And Day
        parameter month: The Month -> int (range[1, 12])
        parameter month_day: The Day Of Month -> int (range[1, 31])
        """

        if type(month) != int or type(month_day) != int:
            raise CalendarError

        if not Date.min_month <= month <= Date.max_month:
            raise CalendarError

        if not Date.min_day <= month_day <= Date.max_day:
            raise CalendarError

        if month == 4 or month == 6 or month == 9 or month == 11:
            if month_day > 30:
                raise CalendarError
        elif month == 2:
            if self._is_leap_year:
                if month_day > 29:
                    raise CalendarError
            elif month_day > 28:
                raise CalendarError

        day = 0
        day += DaysBeforeMonth(4 if self._is_leap_year else 3, month).GetDay()
        day += month_day
        return self.GetWeekdayByYearDay(day)

    @classmethod
    def GetCalendarThisYear(cls):

        """
        GetCalendarThisYear() -> Calendar
        Get The Calendar This Year
        """

        ty = GetYearNow().GetYear()
        date = Date(ty, 1, 1)
        st = date.ToTimeStamp().ToStructTime()
        wd = st.tm_wday
        return cls(wd, Date(ty, 1, 1).IsLeapYear())

    @classmethod
    def GetCalendarByYear(cls, year):

        """
        GetCalendarByYear(year) -> Calendar
        Get A Calendar By Year
        parameter year: A Year -> int
        """

        if type(year) != int:
            raise CalendarError
        wd = Date(year, 1, 1).ToTimeStamp().ToStructTime().tm_wday
        return cls(wd, Date(year, 1, 1).IsLeapYear())


# exceptions (classes)
class Error(Exception):

    """
    Base Class For Exceptions In This Module

    Methods:
        __init__(reason="") -> Error
        __str__() -> str
        __repr__() -> str
        GetReason() -> str

    Properties:
        reason
        __reason (private)
    """

    def __init__(self, reason=""):

        """
        __init__(reason="") -> Error
        Define the property: self.__reason
        """

        self.__reason = reason

    def __str__(self):

        """
        __str__() -> str
        Get The Reason Of The Error
        """

        return self.__reason

    def __repr__(self):

        """
        __repr__() -> str
        Get The Reason Of The Error
        """

        return self.__reason

    @property
    def reason(self):

        """
        Get The Reason Of The Error
        """

        return self.__reason

    def GetReason(self):

        """
        GetReason() -> str
        Get The Reason Of The Error
        """

        return self.__reason


class UnknownError(Error):

    pass


class DateTimeError(Error):

    pass


class TimeTableError(Error):

    pass


class TimerError(Error):
    
    pass


class StartTimerError(TimerError):

    pass


class StopTimerError(TimerError):

    pass


class GetTimeError(Error):

    pass


class TimeUnitError(Error):

    pass


class ParseError(Error):

    pass


class TransformError(Error):

    pass


class TimeStampError(Error):

    pass


class FormatError(Error):

    pass


class DateError(Error):

    pass


class CalendarError(Error):

    pass
