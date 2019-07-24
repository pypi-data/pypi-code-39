"""Date command: A command-based date computation engine

datec allows you to use "date commands" to modify datetime's by adding
to them, like datetime.datetime.now() + Period(2, 'week').

A date command can be parsed from string using the parse() function,
which create a command from a string representation.  This forms the
basis of the datec command, which is a command-line program to output
datetime after applying date commands.  In general the date
representation is NxYYYY-mm-ddTHH:MM:SS.ffffff, where unspecified
parts are omitted leaving the symbols intact, like "2x-2-29T3::." (see
the following for the meaning).  If fractional part is not specified
the "." may be omitted, if all time parts are not specified the "T::."
can be omitted, if all date parts are not specified the "--T" can be
omitted, and if N is 0 the x may be omitted.  By there are a couple
other more formats like +3week and -2wed for shifting by period and
weekday.

Date commands are in two forms: period shifting commands and partial
datetime shifting commands.  The first type is more familiar: they
look like

  +2week (shift the datetime forward by 2 week)
  -1month (shift the datetime backward by 1 month)

Period is one of year, month, week, day, hour, minute and second,
represented by an object of the Period class.  Fractional numbers are
acceptable except for year and month.  If shifting a period leads to
an invalid date (e.g., shift backward 1 month from 2019-07-31), it
moves backwards the closest valid date (here, 2019-06-30).  In general
the parts finer than the shifted part is unaffected (e.g., shifting 1
month from 2019-07-31 02:00 gives you 2019-06-30 02:00).

Partial datetime shifting is less familiar.  It looks like:

  12:: (set the hour number to 12)
  +2x12:: (move forward to the second hour 12)
  +4x--31 (move forward to the fourth occurrence of day 31 of a month)
  -3x-02-29 (move backward to the third occurrence of February 29)
  wed (set to the Wednesday of the same week, week starts on Sunday)
  -3wed (move to the third Wednesday before the current datetime)

They are represented by either a Weekday object or a PartialDate
object with a count.  A count of 0 means setting instead of shifting.
Only integer counts are acceptable.

It is an error to set to an invalid date (e.g., --31 applied on
2019-06-25 is an error).  The datetime parts which are specified must
be consecutive (it is an error to specify 12::05).  It is also an
error to shift for occurrence of partial date with year specified
(e.g., "+2x2019--").

On the other hand, shifting to an invalid date with day number
specified will shift more until a specified date is valid.  For
example, if you add -2-29 with count 1 to 2019-01-01, you end up with
2020-02-29, because 2019-02-29 is not a valid date.  If the count is 2
you get 2024-02-29 instead.

Shifting to invalid date by month will cause the date to moved
backwards until the date is valid.  E.g., if you shift by -6- with
count 1 (next June) from 2019-05-31, you get 2019-06-30.  With count 2
you get 2020-06-30.

This library is grown out of frustration that it is tedious to have a
shell script or program to get a datetime like "the next 6pm from now"
or "the next 3rd of any month from two days ago".  With this module
they can be specified like "+1x18:00:00.0" and "-2day +1x--3"
respectively.  In the expected use cases, counts are small numbers.
So the library is not always efficient (at times we just loop "count"
times to step forward or backward).  Whenever it is simple to do so,
the implementation just forward to relativedelta, in which case they
are more efficient.

At present the program does not handle timezone and daylight saving.
This is bacause the author lives at a place where no daylight saving
is observed.  Contributions are welcome.

"""

import re

import dateutil.relativedelta as dr


__metaclass__ = type


class ParseError(ValueError):
    pass


class Period:
    """Represent a command that shift a number of period

    A period may be a year, month, week, day, hour, minute or second,
    which is the string to be used in the period argument.  If you
    shift by month/year and it ends up into an invalid date, the
    result is "truncated" back to the previous valid day.  Shifting a
    non-integer number of periods is supported except for months and
    years.

    Args:

        count (float): The number of periods to shift
        period (str): The period

    """
    def __init__(self, count, period):
        assert period in ('year', 'month', 'week', 'day',
                          'hour', 'minute', 'second')
        self._count = count
        self._period = period

    def __radd__(self, dt):
        return dt + dr.relativedelta(**{self._period + 's': self._count})

    PARSE_RE = re.compile(r'''
    ^
    (?P<count> [+-] (?: [0-9]+ | [0-9]*\.[0-9]*) )
    (?P<period> year|month|week|day|hour|minute|second)
    $
    ''', re.X)

    @classmethod
    def parse(cls, cmdstr):
        """Parse a command string to a Period object

        The command string should be of the form "<N><period>", where
        <N> is an explicitly signed number, and <period> is a period
        string (case insensitive).

        Args:

            cmdstr (str): The command string

        """
        match = cls.PARSE_RE.match(cmdstr.lower())
        if not match:
            raise ParseError('Cannot parse string %s' % cmdstr)
        gdt = match.groupdict()
        try:
            cnt = int(gdt['count'])
        except Exception:
            cnt = float(gdt['count'])
        return cls(cnt, gdt['period'])


_WEEKDAY_CLS = [dr.SU, dr.MO, dr.TU, dr.WE, dr.TH, dr.FR, dr.SA]
SUN, MON, TUE, WED, THU, FRI, SAT = range(7)
_WEEKDAY_NUM = {'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3,
                'thu': 4, 'fri': 5, 'sat': 6}


class Weekday:
    """Represent a command that set or shift by weekday

    A weekday is a number from 0 to 6, representing Sunday, Monday,
    ..., Friday (the constants SUN, MON, etc. are provided for
    readability of constant weekdays).  If you set a weekday, by using
    a zero count, it moves to the weekday of the current week (week
    always starts on Sunday).  A non-zero (integer) count would
    instead shift forward or backward by that number of occurrences of
    that weekday.  If the original date is already that weekday it is
    not counted as one of those occurrences.

    Args:

        count (int): The number of periods to shift
        day (int): The weekday

    """
    def __init__(self, count, day):
        self._count = count
        assert day in range(7)
        self._day = day
        self._drcls = _WEEKDAY_CLS[day]

    def __radd__(self, dt):
        if self._count > 0:
            return dt + dr.relativedelta(
                days=1, weekday=self._drcls(self._count))
        if self._count < 0:
            return dt + dr.relativedelta(
                days=-1, weekday=self._drcls(self._count))
        dow = (dt.weekday() + 1) % 7
        if self._day < dow:
            return dt + dr.relativedelta(weekday=self._drcls(-1))
        return dt + dr.relativedelta(weekday=self._drcls(1))

    PARSE_RE = re.compile(r'''
    ^
    (?P<count> [+-] (?: [0-9]+ | [0-9]*\.[0-9]*) )?
    (?P<weekday> sun|mon|tue|wed|thu|fri|sat)
    $
    ''', re.X)

    @classmethod
    def parse(cls, cmdstr):
        """Parse a command string to a Weekday object

        The command string should be of the form "<N><weekday>", where
        <N> is an explicitly signed number or empty string
        (representing 0), and <weekday> is a weekday 3-letter string
        like sun, mon, etc (case insensitive).

        Args:

            cmdstr (str): The command string

        """
        match = cls.PARSE_RE.match(cmdstr.lower())
        if not match:
            raise ParseError('Cannot parse string %s' % cmdstr)
        gdt = match.groupdict()
        cnt = int(gdt['count']) if gdt['count'] else 0
        return cls(cnt, _WEEKDAY_NUM[gdt['weekday']])


class PartialDate:
    """Represent a command that set or shift by partial date

    A partial date command specifies a count and the values of some of
    year, month, day, hour, minute, second and microsecond.  The
    specified value must be contiguous among the parts above.

    Using a count of 0 sets the specified fields.  It raises an error
    if the result is an invalid date.

    Using a positive or negative count shift the date forward or
    backward, and in this case the year must not be specified.  It
    only counts valid dates.  E.g., you can shift forward by a certain
    number of Feb 29.  The exception is when setting the month only.
    In that case, if the result is an invalid date, the date is
    "truncated" to the last valid date.

    Args:

        count (int): The number of periods to shift
        year (int): The year number
        month (int): The month number (1 to 12)
        day (int): The day number (1 to 31)
        hour (int): The hour number (0 to 23)
        minute (int): The minute number (0 to 59)
        second (int or float): The second number (0 to smaller than 60)
        microsecond (int): The microsecond number (0 to 999999)

    """

    _INVALID_SIG_RE = re.compile('10+1')

    def __init__(self, count=0, year=None, month=None, day=None,
                 hour=None, minute=None, second=None, microsecond=None):
        assert not count or not year, 'Absolute date with non-zero count'
        assert not isinstance(second, float) or \
            microsecond is None, 'Doubly specified microsecond'
        vals = [year, month, day, hour, minute, second, microsecond]
        sig = ''.join([("0" if v is None else "1") for v in vals])
        assert not self._INVALID_SIG_RE.search(sig), \
            'Non-consecutive components'
        if isinstance(second, float):
            second, orig_second = int(second), second
            microsecond = int((orig_second - second) * 1000000 + 0.5)
        self._count = count
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._firstset = sig.find('1')

    _FIRSTSET_MOD = [
        '', 'years', 'months', 'days', 'hours', 'minutes', 'seconds'
    ]

    def __radd__(self, dt):
        if self._firstset == -1:
            return dt
        if not(self._count):
            return self._rset(dt)
        # modify day or finer, or day specified and is not vulnerable
        # to variable month length
        if self._firstset > 2 or \
           (self._day is not None and self._day <= 28):
            return self._simpleshift(dt)
        if self._day is None:
            return self._monthshift(dt)
        return self._dayshift(dt)

    def _rset(self, dt):
        updater = {'year': self._year,
                   'month': self._month,
                   'day': self._day,
                   'hour': self._hour,
                   'minute': self._minute,
                   'second': self._second,
                   'microsecond': self._microsecond}
        updater = {k: v for k, v in updater.items() if v is not None}
        return dt.replace(**updater)

    def _simpleshift(self, dt):
        remain = self._count
        ret = self._rset(dt)
        if self._count < 0:
            if ret < dt:
                remain += 1
        else:
            if ret > dt:
                remain -= 1
        mod_field = self._FIRSTSET_MOD[self._firstset]
        return ret + dr.relativedelta(**{mod_field: remain})

    def _dayshift(self, dt):
        # Day specified
        if self._firstset == 2:  # modify month
            shift = dr.relativedelta(months=1 if self._count > 0 else -1)
            limit = 2  # Must be able to find a 31st day in 2 months
        else:
            shift = dr.relativedelta(years=1 if self._count > 0 else -1)
            limit = 8  # Must be able to find a Feb 29 in 8 years
        count = abs(self._count)
        # Find first date
        curr = dt
        for _ in range(limit):
            try:
                ret = self._rset(curr)
            except ValueError:
                curr += shift
                continue
            if (self._count > 0) == (ret > dt):
                count -= 1
            break
        else:
            raise ValueError('Failed day shifting: invalid date?')
        # Find count occurrences
        while True:
            if count == 0:
                return ret
            ret += shift
            try:
                ret = self._rset(ret)
            except ValueError:
                continue
            count -= 1

    def _monthshift(self, dt):
        # Only month specified, shift by month rather than by year
        if self._count > 0:
            num_months = self._month - dt.month
            sign = 1
        else:
            num_months = dt.month - self._month
            sign = -1
        if num_months <= 0:
            num_months += 12
        num_months += (abs(self._count) - 1) * 12
        return dt + dr.relativedelta(months=sign * num_months)

    PARSE_RE1 = re.compile(r'''
    ^
    (?: (?P<count> [+-] (?: [0-9]+ | [0-9]*\.[0-9]*) ) x)?
    (?P<year> [0-9]*)
    -
    (?P<month> [0-9]*)
    -
    (?P<day> [0-9]*)
    $
    ''', re.X)

    PARSE_RE2 = re.compile(r'''
    ^
    (?: (?P<count> [+-] (?: [0-9]+ | [0-9]*\.[0-9]*) ) x)?
    (?:
      (?P<year> [0-9]*)
      -
      (?P<month> [0-9]*)
      -
      (?P<day> [0-9]*)
      t
    )?
    (?P<hour> [0-9]*)
    :
    (?P<minute> [0-9]*)
    :
    (?P<second> [0-9]*)
    (?:\. (?P<microsecond> [0-9]*) )?
    $
    ''', re.X)

    @classmethod
    def parse(cls, cmdstr):
        """Parse a command string to a PartialDate object

        The command string should be of the form
        "<N>x<year>-<month>-<day>T<hour>:<minute>:<second>.<micro>",
        where <N> is an explicitly signed number or empty string
        (representing 0).  To skip the specification of a part use
        empty string.  If all date parts are not specified the "--T"
        may be omitted.  If all the time parts are not specified the
        "T::." may be omitted.  If the microsecond part is not
        specified the "." part may be omitted.

        Args:

            cmdstr (str): The command string

        """
        match = cls.PARSE_RE1.match(cmdstr.lower())
        if not match:
            match = cls.PARSE_RE2.match(cmdstr)
        if not match:
            raise ParseError('Cannot parse string %s' % cmdstr)
        gdt = match.groupdict()

        def _matchval(key):
            val = gdt.get(key)
            if not val:
                return None
            return int(val)

        microsecond = None
        msval = gdt.get('microsecond')
        if msval:
            microsecond = int(msval.ljust(6, '0')[:6])
        return cls(_matchval('count') or 0,
                   _matchval('year'),
                   _matchval('month'),
                   _matchval('day'),
                   _matchval('hour'),
                   _matchval('minute'),
                   _matchval('second'),
                   microsecond)


def parse(cmdstr):
    """Attempt to parse one of the possible date command

    Args:

        cmdstr (str): The command string

    """
    try:
        return Period.parse(cmdstr)
    except ParseError:
        pass
    try:
        return Weekday.parse(cmdstr)
    except ParseError:
        pass
    return PartialDate.parse(cmdstr)
